#! /usr/bin/env python
# coding=utf-8
import cv2
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
import json
from absl import app, flags, logging
from absl.flags import FLAGS
import numpy as np
import colorsys
import random

flags.DEFINE_string('detect_type', 'image', 'image or video')
flags.DEFINE_string('file', './test.jpg', 'path to input image or video')

def loadImage(frame):
    input_size = 416
    # read image
    original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # image resize
    image_data = cv2.resize(original_image, (input_size, input_size))
    image_data = image_data / 255.
    # convert data type
    images_data = []
    for i in range(1):
        images_data.append(image_data)
    images_data = np.asarray(images_data).astype(np.float32)
    return images_data, original_image


# load config
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

saved_model_loaded = tf.saved_model.load('rubbish', tags=[tag_constants.SERVING])
infer = saved_model_loaded.signatures['serving_default']
    
def read_class_names(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names
    
def detect_video(VEDIO_PATH):
    '''
    infer: the loaded model object
    '''
    # detect video
    vid = cv2.VideoCapture(VEDIO_PATH)
    return_value, frame = vid.read()
    n = 0
    while return_value:
        if n % 3 == 0:
            image_data, original_image = loadImage(frame)
            detect(image_data, original_image)
        return_value, frame = vid.read()
        if cv2.waitKey(1) & 0xFF == ord('q'): break


def detect_pic(img):
    # detect picture
    img = cv2.imread(img)
    image_data, original_image = loadImage(img)
    detect(image_data, original_image)
    
    
def detect(images_data, original_image):
    # predict
    batch_data = tf.constant(images_data)
    pred_bbox = infer(batch_data)
    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]
    # get original box size
    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=20,
        max_total_size=20,
        iou_threshold=0.45,
        score_threshold=0.20
    )
    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
    # show detected pic
    draw_bbox(original_image, pred_bbox)
        
def draw_bbox(image, bboxes, classes=read_class_names('rubbish.names'), show_label=True):
    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    random.seed(0)
    random.shuffle(colors)
    random.seed(None)
    out_boxes, out_scores, out_classes, num_boxes = bboxes
    for i in range(num_boxes[0]):
        if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
        coor = out_boxes[0][i]
        coor[0] = int(coor[0] * image_h)
        coor[2] = int(coor[2] * image_h)
        coor[1] = int(coor[1] * image_w)
        coor[3] = int(coor[3] * image_w)
        score = float(out_scores[0][i])
        fontScale = 0.5
        class_ind = int(out_classes[0][i])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[1], coor[0]), (coor[3], coor[2])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)
        if show_label:
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=bbox_thick // 2)[0]
            c3 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
            cv2.rectangle(image, c1, (np.float32(c3[0]), np.float32(c3[1])), bbox_color, -1) #filled

            cv2.putText(image, bbox_mess, (c1[0], np.float32(c1[1] - 2)), cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale, (0, 0, 0), bbox_thick // 2, lineType=cv2.LINE_AA)
    if FLAGS.detect_type == 'image':
        cv2.imwrite("result.jpg", image)
    cv2.imshow('result', image)
    
def main(_argv):
    if FLAGS.detect_type == 'image':
        detect_pic(FLAGS.file)
    else:
        detect_video(FLAGS.file)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
