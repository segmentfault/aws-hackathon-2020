import os
import cv2

# 加载猫脸检测器,此处使用haarcascade_frontalcatface.xml
catPath = "haarcascade_frontalcatface.xml"
faceCascade = cv2.CascadeClassifier(catPath)

# 加载数据
def process_data():
    names = os.listdir('./data')
    names = [n for n in names if not n.startswith('.')]
    for name in names:
        for i in range(1,7):
            # 读取图片并灰度化
            save_path = './train_data/%s/%d.png'%(name,i)
            img = cv2.imread('./data/%s/%d.png'%(name,i))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 猫脸检测
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.01,
                minNeighbors=3,
                minSize=(150, 150),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            for (x, y, w, h) in faces:
                face = img[y:y + h, x:x + w]
                face = cv2.resize(face, dsize=(256, 256))
                print(save_path)
                cv2.imwrite(save_path, face)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, 'Cat', (x, y - 7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            # 显示图片并保存
            cv2.imshow('Cat?', img)
            cv2.imwrite("cat.jpg", img)
            c = cv2.waitKey(10)
    return

if __name__ == '__main__':

    process_data()

