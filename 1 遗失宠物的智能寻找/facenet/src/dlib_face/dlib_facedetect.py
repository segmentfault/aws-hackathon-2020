import os
import cv2
import dlib
import glob

im_floder = ''
crop_im_path = ''

im_floder_list = glob.glob(im_floder + '/*')
detector = dlib.get_frontal_face_detector()
idx = 0

for idx_floder in im_floder_list:
    im_floder_list = glob.glob(idx_floder + '/*')

    if not os.path.exists('{}/{}'.format(crop_im_path, idx)):
        os.mkdir('{}/{}'.format(crop_im_path, idx))

    idx_im = 0
    for im_path in im_floder_list:
        im_data = cv2.imread(im_path)
        dets = detector(im_data, 1)
        print(dets)
        if dets.__len__() == 0:
            continue
        d = dets[0]
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()

        y1 = int(y1 - (y2 - y1) * 0.3)
        x1 = int(x1 - (x2 - x1) * 0.05)
        x2 = int(x2 + (x2 - x1) * 0.05)

        im_crop_data = im_data[y1:y2, x1:x2]
        im_data = cv2.resize(im_crop_data, (160, 160))

        im_save_path = '{}/{}/{}_{}.jpg'.format(crop_im_path, idx, idx, "%04d" % idx_im)
        cv2.imwrite(im_save_path, im_data)
        idx_im += 1
    idx += 1
