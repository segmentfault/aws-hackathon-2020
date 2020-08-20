import os
import uuid

from flask_cors import CORS
from gevent import pywsgi
from flask import Flask
from flask import abort
import tensorflow as tf
import numpy as np

from boto3.session import Session
session = Session(aws_access_key_id='', aws_secret_access_key='', region_name='ap-northeast-1')
s3 = session.client("s3")

app = Flask(__name__)
model = tf.keras.models.load_model('model')

def classfy(path, filename):
    # IMG_SHAPE = (None, 256, 256, 3)
    # model.build(IMG_SHAPE)
    unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[-1]
    try:
        s3.download_file(Filename=unique_filename, Key=path+'/'+filename, Bucket='fzhcats')
    except:
        return -1
    else:
        # 读取图片
        img_raw = tf.io.read_file(unique_filename)
        os.remove(unique_filename)
        # 解码图片
        img_tensor = tf.image.decode_jpeg(img_raw, channels=3)
        # 统一图片大小
        img_tensor = tf.image.resize_with_pad(img_tensor, 256, 256)
        # 转换数据类型
        img_tensor = tf.cast(img_tensor, tf.float32)
        # 归一化
        img = img_tensor / 255
        X = np.array([np.asarray(img)])

        return model.predict_classes(X)[0]

@app.route('/classify/<path>/<filename>')
def hello_world(path, filename):
    code = classfy(path, filename)
    if code == -1:
        abort(500)
    return str(code)

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()