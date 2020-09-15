from sklearn.svm import SVC
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
# 加载数据
def load_data():
    names = os.listdir('./train_data')
    #print(names)
    names = [n for n in names if not n.startswith('.')]
    X = []
    y = np.asarray([i for i in range(len(names))]*6)
    y.sort()
    for name in names:
        for i in range(1,7):
            #print('./train_data/%s/%d.png'%(name,i))
            gray = cv2.imread('./train_data/%s/%d.png'%(name,i))
            gray = cv2.resize(gray, dsize=(256, 256)) # 尺寸统一标准
            X.append(gray)
    # 将列表变成了数组
    return np.asarray(X),y,names
if __name__ == '__main__':
    # 1、加载数据
    X,y,names = load_data()
    print(X.shape)
    # 2、数据拆分，训练数据和测试数据
    X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=512)

    # 3、声明SVM
    svc = SVC(kernel='rbf')

    # 4、预测
    print('---------------',X_train.shape)
    print('---------------',y_train.shape)
    X_train = X_train.reshape(13,-1)
    svc.fit(X_train,y_train)

    # 5、预测
    print(X_test.shape)
    X_test = X_test.reshape(5,196608) # 倒着数，有多少填充多少
    score = svc.score(X_test,y_test)
    print('喵脸验证，准确率：',score)
    y_pred = svc.predict(X_test) # 预测值

    # 6、数据展示，可视化
    for face,y_ in zip(X_test,y_pred):
        face = face.reshape(256, 256, 3)
        label = names[y_]
        cv2.putText(face,text = label,
                    org = (15,15),
                    fontFace=cv2.FONT_ITALIC,
                    fontScale=0.8,color=[255,0,0],thickness=1)
        cv2.imshow('face',face)
        key = cv2.waitKey(3000)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
