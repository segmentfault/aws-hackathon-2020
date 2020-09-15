import random
import colorsys
import cv2
import threading
import os
import numpy as np

from tools.transform import *


class Decode(object):
    def __init__(self, exe, program, all_classes, cfg, for_test=True):
        self.all_classes = all_classes
        self.num_classes = len(self.all_classes)
        self.exe = exe
        self.program = program

        # 图片预处理
        self.context = cfg.context
        # sample_transforms
        self.to_rgb = cfg.decodeImage['to_rgb']
        self.normalizeImage = NormalizeImage(**cfg.normalizeImage)  # 先除以255归一化，再减均值除以标准差
        target_size = cfg.eval_cfg['target_size']
        max_size = cfg.eval_cfg['max_size']
        if for_test:
            target_size = cfg.test_cfg['target_size']
            max_size = cfg.test_cfg['max_size']
        self.resizeImage = ResizeImage(target_size=target_size,
                                       max_size=max_size,
                                       interp=cfg.resizeImage['interp'],
                                       use_cv2=cfg.resizeImage['use_cv2'])  # 多尺度训练，随机选一个尺度，不破坏原始宽高比地缩放。具体见代码。
        self.permute = Permute(**cfg.permute)  # 图片从HWC格式变成CHW格式
        # batch_transforms
        self.padBatch = PadBatch(**cfg.padBatch)  # 由于ResizeImage()的机制特殊，这一批所有的图片的尺度不一定全相等，所以这里对齐。

    # 处理一张图片
    def detect_image(self, image, fetch_list, draw_image, draw_thresh=0.0):
        pimage, im_info = self.process_image(np.copy(image))

        boxes, scores, classes = self.predict(pimage, im_info, fetch_list, draw_thresh)
        if len(scores) > 0 and draw_image:
            self.draw(image, boxes, scores, classes)
        return image, boxes, scores, classes

    # 处理一批图片
    def detect_batch(self, batch_img, fetch_list, draw_image, draw_thresh=0.0):
        batch_size = len(batch_img)
        result_image, result_boxes, result_scores, result_classes = [None] * batch_size, [None] * batch_size, [None] * batch_size, [None] * batch_size
        batch = []
        batch_im_info = []

        for image in batch_img:
            pimage, im_info = self.process_image(np.copy(image))
            batch.append(pimage)
            batch_im_info.append(im_info)
        batch = np.concatenate(batch, axis=0)
        batch_im_info = np.concatenate(batch_im_info, axis=0)
        results = self.exe.run(self.program, feed={"image": batch, "im_info": batch_im_info, }, fetch_list=fetch_list, return_numpy=False)
        pred = np.array(results[0])  # [M, 6]
        if pred[0][0] < 0.0:
            boxes = np.array([])
            classes = np.array([])
            scores = np.array([])
        else:
            boxes = pred[:, 2:]
            scores = pred[:, 1]
            classes = pred[:, 0].astype(np.int32)

            pos = np.where(scores >= draw_thresh)
            boxes = boxes[pos]       # [M, 4]
            classes = classes[pos]   # [M, ]
            scores = scores[pos]     # [M, ]
        if len(scores) > 0 and draw_image:
            self.draw(batch_img[0], boxes, scores, classes)
        result_image[0] = batch_img[0]
        result_boxes[0] = boxes
        result_scores[0] = scores
        result_classes[0] = classes
        return result_image, result_boxes, result_scores, result_classes

    def draw(self, image, boxes, scores, classes):
        image_h, image_w, _ = image.shape
        # 定义颜色
        hsv_tuples = [(1.0 * x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

        random.seed(0)
        random.shuffle(colors)
        random.seed(None)

        for box, score, cl in zip(boxes, scores, classes):
            x0, y0, x1, y1 = box
            left = max(0, np.floor(x0 + 0.5).astype(int))
            top = max(0, np.floor(y0 + 0.5).astype(int))
            right = min(image.shape[1], np.floor(x1 + 0.5).astype(int))
            bottom = min(image.shape[0], np.floor(y1 + 0.5).astype(int))
            bbox_color = colors[cl]
            # bbox_thick = 1 if min(image_h, image_w) < 400 else 2
            bbox_thick = 1
            cv2.rectangle(image, (left, top), (right, bottom), bbox_color, bbox_thick)
            bbox_mess = '%s: %.2f' % (self.all_classes[cl], score)
            t_size = cv2.getTextSize(bbox_mess, 0, 0.5, thickness=1)[0]
            cv2.rectangle(image, (left, top), (left + t_size[0], top - t_size[1] - 3), bbox_color, -1)
            cv2.putText(image, bbox_mess, (left, top - 2), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 0), 1, lineType=cv2.LINE_AA)

    def process_image(self, img):
        if self.to_rgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        context = self.context
        sample = {}
        sample['image'] = img
        sample['h'] = img.shape[0]
        sample['w'] = img.shape[1]

        sample = self.normalizeImage(sample, context)
        sample = self.resizeImage(sample, context)
        sample = self.permute(sample, context)
        samples = self.padBatch([sample], context)

        pimage = np.expand_dims(samples[0]['image'], axis=0)
        im_info = np.expand_dims(samples[0]['im_info'], axis=0)
        return pimage, im_info

    def predict(self, image, im_info, fetch_list, draw_thresh):
        results = self.exe.run(self.program, feed={"image": image, "im_info": im_info, }, fetch_list=fetch_list, return_numpy=False)
        pred = np.array(results[0])   # [M, 6]
        if pred[0][0] < 0.0:
            boxes = np.array([])
            classes = np.array([])
            scores = np.array([])
        else:
            boxes = pred[:, 2:]
            scores = pred[:, 1]
            classes = pred[:, 0].astype(np.int32)

            pos = np.where(scores >= draw_thresh)
            boxes = boxes[pos]         # [M, 4]
            classes = classes[pos]     # [M, ]
            scores = scores[pos]       # [M, ]
        return boxes, scores, classes

    def _nms_boxes(self, boxes, scores):
        x = boxes[:, 0]
        y = boxes[:, 1]
        w = boxes[:, 2] - x
        h = boxes[:, 3] - y

        areas = w * h
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)

            xx1 = np.maximum(x[i], x[order[1:]])
            yy1 = np.maximum(y[i], y[order[1:]])
            xx2 = np.minimum(x[i] + w[i], x[order[1:]] + w[order[1:]])
            yy2 = np.minimum(y[i] + h[i], y[order[1:]] + h[order[1:]])

            w1 = np.maximum(0.0, xx2 - xx1 + 1)
            h1 = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w1 * h1

            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= self._t2)[0]
            order = order[inds + 1]

        keep = np.array(keep)

        return keep


    def _fcos_out(self, pred_boxes, pred_scores):
        '''
        :param pred_boxes:   [所有格子, 4]，最终坐标
        :param pred_scores:  [80, 所有格子]，最终分数
        :return:
        '''
        # 分数过滤
        box_classes = np.argmax(pred_scores, axis=0)
        box_class_scores = np.max(pred_scores, axis=0)
        pos = np.where(box_class_scores >= self._t1)

        boxes = pred_boxes[pos]         # [M, 4]
        classes = box_classes[pos]      # [M, ]
        scores = box_class_scores[pos]  # [M, ]


        nboxes, nclasses, nscores = [], [], []
        for c in set(classes):
            inds = np.where(classes == c)
            b = boxes[inds]
            c = classes[inds]
            s = scores[inds]

            keep = self._nms_boxes(b, s)

            nboxes.append(b[keep])
            nclasses.append(c[keep])
            nscores.append(s[keep])

        if not nclasses and not nscores:
            return None, None, None

        boxes = np.concatenate(nboxes)
        classes = np.concatenate(nclasses)
        scores = np.concatenate(nscores)

        return boxes, scores, classes