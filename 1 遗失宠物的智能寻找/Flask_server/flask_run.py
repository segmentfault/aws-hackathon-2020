from flask import Flask, request
import os
import numpy as np
import cv2
from gevent import monkey
import tensorflow as tf

from Facenet.facenet import prewhiten

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

monkey.patch_all()

app = Flask(__name__)

PATH_TO_FROZEN_GRAPH = ''
PATH_TO_LABELS = ''
IMAGE_SIZE = (256, 256)
detection_sess = tf.Session()

with detection_sess.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        ops = tf.get_default_graph().get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in [
            'num_detections', 'detection_boxes', 'detection_scores',
            'detection_classes', 'detection_masks'
        ]:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                    tensor_name)
        if 'detection_masks' in tensor_dict:
            # The following processing is only for single image
            detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
            detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
            # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
            real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
            detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
            detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                detection_masks, detection_boxes, IMAGE_SIZE[0], IMAGE_SIZE[1])
            detection_masks_reframed = tf.cast(
                tf.greater(detection_masks_reframed, 0.5), tf.uint8)
            # Follow the convention by adding back the batch dimension
            tensor_dict['detection_masks'] = tf.expand_dims(
                detection_masks_reframed, 0)
        image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

# ##########################################################
# face feature
face_feature_sess = tf.Session()
ff_pb_path = 'Facenet/face_recognition_model.pb'

with face_feature_sess.as_default():
    ff_od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(ff_pb_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        ops = tf.get_default_graph().get_operations()

        ff_images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        ff_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        ff_embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")


@app.route("/")
def helloworld():
    return '<h1>Web Service</h1><br><h3>Authored by Bryce</h3>'


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    f = request.files.get('file')
    # print(f)
    upload_path = os.path.join('object_detection/tmp/' + f.filename)
    # print(upload_path)
    f.save(upload_path)
    return upload_path


@app.route("/face_detect")
def inference():
    im_url = request.args.get("url")
    im_data = cv2.imread(im_url)
    sp = im_data.shape
    im_data_re = cv2.resize(im_data, IMAGE_SIZE)
    output_dict = detection_sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(im_data_re, 0)})

    # all outputs are float32 numpy arrays, so convert types as appropriate
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    for i in range(len(output_dict['detection_scores'])):
        if output_dict['detection_scores'][i] > 0.1:
            bbox = output_dict['detection_boxes'][i]
            y1 = bbox[0]
            x1 = bbox[1]
            y2 = (bbox[2])
            x2 = (bbox[3])
            print(output_dict['detection_scores'][i], x1, y1, x2, y2)

    return str([x1, y1, x2, y2])


def read_image(path):
    im_data = cv2.imread(path)
    im_data = prewhiten(im_data)
    im_data = cv2.resize(im_data, (160, 160))
    # 1 * h * w * 3
    return im_data


@app.route("/face_dis")
def face_feature():
    im_data1 = read_image('')
    im_data1 = np.expand_dims(im_data1, axis=0)
    emb1 = face_feature_sess.run(ff_embeddings,
                                 feed_dict={ff_images_placeholder: im_data1, ff_train_placeholder: False})
    im_data2 = read_image('')
    im_data2 = np.expand_dims(im_data2, axis=0)
    emb2 = face_feature_sess.run(ff_embeddings,
                                 feed_dict={ff_images_placeholder: im_data2, ff_train_placeholder: False})

    dis = np.linalg.norm(emb2 - emb1)

    return str(dis)


@app.route("/face_register", methods=['POST', 'GET'])
def face_register():

    f = request.files.get('file')
    print(f)
    upload_path = os.path.join('object_detection/tmp/' + f.filename)
    print(upload_path)
    f.save(upload_path)


    im_data = cv2.imread(upload_path)
    sp = im_data.shape
    im_data_re = cv2.resize(im_data, IMAGE_SIZE)
    output_dict = detection_sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(im_data_re, 0)})

    # all outputs are float32 numpy arrays, so convert types as appropriate
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]

    global mess
    for i in range(len(output_dict['detection_scores'])):
        if output_dict['detection_scores'][i] > 0.1:
            bbox = output_dict['detection_boxes'][i]
            y1 = bbox[0]
            x1 = bbox[1]
            y2 = (bbox[2])
            x2 = (bbox[3])
            print(output_dict['detection_scores'][i], x1, y1, x2, y2)


            y1 = int(y1 * sp[0])
            x1 = int(x1 * sp[1])
            y2 = int(y2 * sp[0])
            x2 = int(x2 * sp[1])
            face_data = im_data[y1:y2, x1:x2]  
            im_data = prewhiten(face_data)
            im_data = cv2.resize(im_data, (160, 160))
            im_data = np.expand_dims(im_data, axis=0)

            emb1 = face_feature_sess.run(ff_embeddings,
                                         feed_dict={ff_images_placeholder: im_data, ff_train_placeholder: False})
            strr = ",".join(str(i) for i in emb1[0])

            with open('face/feature.txt', 'w') as f:
                f.writelines(strr)
            mess = 'success'
            break
        else:
            mess = 'fail'

    return mess


@app.route("/face_login", methods=['POST', 'GET'])
def face_login()
    f = request.files.get('file')
    print(f)
    upload_path = os.path.join('object_detection/tmp/login_tmp.' + f.filename.split(".")[-1])
    print(upload_path)
    f.save(upload_path)

    im_data = cv2.imread(upload_path)
    sp = im_data.shape
    im_data_re = cv2.resize(im_data, IMAGE_SIZE)
    output_dict = detection_sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(im_data_re, 0)})

  
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]
    global mess
    for i in range(len(output_dict['detection_scores'])):
        if output_dict['detection_scores'][i] > 0.1:
            bbox = output_dict['detection_boxes'][i]
            y1 = bbox[0]
            x1 = bbox[1]
            y2 = (bbox[2])
            x2 = (bbox[3])
            print(output_dict['detection_scores'][i], x1, y1, x2, y2)


            y1 = int(y1 * sp[0])
            x1 = int(x1 * sp[1])
            y2 = int(y2 * sp[0])
            x2 = int(x2 * sp[1])
            face_data = im_data[y1:y2, x1:x2]  
            im_data = prewhiten(face_data)
            im_data = cv2.resize(im_data, (160, 160))
            im_data = np.expand_dims(im_data, axis=0)

            emb1 = face_feature_sess.run(ff_embeddings,
                                         feed_dict={ff_images_placeholder: im_data, ff_train_placeholder: False})
            with open('face/feature.txt') as f:
                fea_str = f.readlines()
            emb2_str = fea_str[0].split(",")
            emb2 = []
            for ss in emb2_str:
                emb2.append(float(ss))
            emb2 = np.array(emb2)

            dist = np.linalg.norm(emb1 - emb2)
            print('dist----------------->', dist)
            if dist < 0.3:
                return 'success'
            else:
                return 'fail'
    return 'fail'


if __name__ == '__main__':
    app.run(host='192.168.0.110', port=90, debug=True)
