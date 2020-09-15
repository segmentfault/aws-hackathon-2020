#! /usr/bin/env python
# coding=utf-8
from collections import deque
import datetime
import cv2
import os
import time
import numpy as np
import tensorflow as tf
import keras.layers as layers
from tools.cocotools import get_classes
from model.yolov4 import YOLOv4
from model.decode_np import Decode

import logging
FORMAT = '%(asctime)s-%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)



# 6G的卡，训练时如果要预测，则设置use_gpu = False，否则显存不足。
use_gpu = False
#use_gpu = True

# 显存分配。
if use_gpu:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
else:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 1.0
set_session(tf.Session(config=config))


if __name__ == '__main__':

    classes_path = 'coco_classes.txt'
    model_path = 'yolov4.h5'
    input_shape = (416, 416)
    # 验证时的分数阈值和nms_iou阈值
    conf_thresh = 0.05
    nms_thresh = 0.45

    # 是否给图片画框
    draw_image = True
    # draw_image = False


    num_anchors = 3
    all_classes = get_classes(classes_path)
    num_classes = len(all_classes)
    inputs = layers.Input(shape=(None, None, 3))
    yolo = YOLOv4(inputs, num_classes, num_anchors)
    yolo.load_weights(model_path, by_name=True)

    _decode = Decode(conf_thresh, nms_thresh, input_shape, yolo, all_classes)

    if not os.path.exists('images/res/'): os.mkdir('images/res/')
    if not os.path.exists('images/res_lr/'): os.mkdir('images/res_lr/')

    path_dir = os.listdir('images/test')
    # warm up
    if use_gpu:
        for k, filename in enumerate(path_dir):
            image = cv2.imread('images/test/' + filename)
            image, boxes, scores, classes = _decode.detect_image(image, draw_image=False)
            if k == 10:
                break


    time_stat = deque(maxlen=20)
    start_time = time.time()
    end_time = time.time()
    num_imgs = len(path_dir)
    start = time.time()
    for k, filename in enumerate(path_dir):
        image = cv2.imread('images/test/' + filename)
        image, boxes, scores, classes = _decode.detect_image(image, draw_image)
        print(boxes)
        catdog = []
        for (x, y, x2, y2) in boxes:
            x = int(x)
            y = int(y)
            x2 = int(x2)
            y2 = int(y2)
            catdog.append(image[y:y2, x:x2])

        # 估计剩余时间
        start_time = end_time
        end_time = time.time()
        time_stat.append(end_time - start_time)
        time_cost = np.mean(time_stat)
        eta_sec = (num_imgs - k) * time_cost
        eta = str(datetime.timedelta(seconds=int(eta_sec)))

        logger.info('Infer iter {}, num_imgs={}, eta={}.'.format(k, num_imgs, eta))
        if draw_image:
            cv2.imwrite('images/res/' + filename, image)
            i = 0
            for cd in catdog:
                cv2.imwrite('images/res_lr/'+ str(i) + filename, cd)
                i += 1
            logger.info("Detection bbox results save in images/res/{}".format(filename))
    cost = time.time() - start
    logger.info('total time: {0:.6f}s'.format(cost))
    logger.info('Speed: %.6fs per image,  %.1f FPS.'%((cost / num_imgs), (num_imgs / cost)))


