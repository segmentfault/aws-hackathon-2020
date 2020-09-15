import os  # 处理字符串路径
import glob  # 查找文件
from keras.models import Sequential  # 导入Sequential模型
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
import numpy as np
from pandas import Series, DataFrame
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils, plot_model
from six.moves import range
#加载数据
import os
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
#读取文件夹train下的42000张图片，图片为彩色图，所以为3通道，
#如果是将彩色图作为输入,图像大小224*224
def load_data():
    path = "D:\cat\91"
    files = os.listdir(path)
    print(len(files))
    images = []
    labels = []
    num = 64
    t = 0
    for f in files:
        img_path = path + '/' + f
        j = f.split(".")[0]
        if '_' in j:
            j = int(j.split("_")[0])
        else:
            j = int(j)

        from keras.preprocessing import image    
        img = image.load_img(img_path, target_size=(128, 128))
        img_array = image.img_to_array(img)
        images.append(img_array)
        if j > 8:
            labels.append(1)
        else:
            labels.append(0)
        t += 1
 
    data = np.array(images)
    labels = np.array(labels)
 
    # label = np_utils.to_categorical(labels, 2)
    return data, labels ,images

data,label,images = load_data()

print(data.shape)
train_data = data[:55]
train_labels = label[:55]
validation_data = data[55:]
validation_labels = label[55:]
# images = images / 255
for i in range(len(images)):
    if i>55:
        plt.imsave(r"D:\cat\96\1\validation_{}.jpg".format(i), images[i]/255)
    else:
        plt.imsave(r"D:\cat\96\2\train_{}.jpg".format(i), images[i]/255)    
model = Sequential()
#第一个卷积层，4个卷积核，每个卷积核大小5*5。
#激活函数用tanh
#你还可以在model.add(Activation('tanh'))后加上dropout的技巧: model.add(Dropout(0.5))
model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
#第二个卷积层，8个卷积核，每个卷积核大小3*3。
#激活函数用tanh
#采用maxpooling，poolsize为(2,2)
model.add(Convolution2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#第三个卷积层，16个卷积核，每个卷积核大小3*3
#激活函数用tanh
#采用maxpooling，poolsize为(2,2)
model.add(Convolution2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#全连接层，先将前一层输出的二维特征图flatten为一维的。

model.add(Flatten())
model.add(Dense(512, activation='relu'))
#sigmoid分类，输出是2类别
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['acc'])

history = model.fit(train_data, train_labels,
          epochs=50, batch_size=100,
          validation_data=(validation_data, validation_labels))

import matplotlib.pyplot as plt
# 调整像素值
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_dir = "D:/cat/96/2"
train_generator = train_datagen.flow_from_directory(
    directory=train_dir,
    target_size=(128, 128),
    batch_size=20,
    class_mode='binary')

validation_dir="D:/cat/96/1"
validation_generator = test_datagen.flow_from_directory(
    directory=validation_dir,
    target_size=(128, 128),
    batch_size=20,
    class_mode='binary')

history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=30,
    validation_data=validation_generator,
    validation_steps=50)

model.save('cats_and_dogs_small_1.h5')
os.environ["PATH"]+=os.pathsep + "D:/graphviz-2.38/release/bin/"
plot_model(model, to_file='model.png', show_shapes=True)

def plot_acc_loss_curve(history):
    # 显示训练集和验证集的acc和loss曲线
    from matplotlib import pyplot as plt
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()
    #plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    #plt.grid()
    plt.show()

plot_acc_loss_curve(history)
