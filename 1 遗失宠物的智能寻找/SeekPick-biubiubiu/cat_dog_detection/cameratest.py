from yolov3_model import *
def plot_info(img,x,y,info):
    cv2.putText(img, info, (x, y), 0, 0.5, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
    return img


def fix_outOFrange(det,h,w):
    det = np.where(det<0,0,det)
    det[:, [1,3]] = np.where(det[:, [1,3]] > h - 1, h - 1, det[:, [1,3]])
    det[:, [0,2]] = np.where(det[:, [0,2]] > w - 1, w - 1, det[:, [0,2]])
    return det

if __name__ == '__main__':
    yolo_cfg_path = 'coco_cfg/'
    device = torch.device('cuda:0')
    cfg = yolo_cfg_path + 'yolov3.cfg'
    weights = yolo_cfg_path + 'yolov3.pt'
    name_path = yolo_cfg_path + "coco.names"
    f = open(name_path)
    names = [i.strip() for i in f.readlines()]
    labelmap = dict(enumerate(names))
    f.close()

    yolo_dectection = YOLO_Dectection(device=device, cfg_path=cfg, weights_path=weights)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame,1)   #镜像操作
        det = yolo_dectection.detect(frame)
        # print(det)
        if det is not None:
            # det = np.where(det < 0, 0, det)
            for *xyxy, conf, cls in det:
                label = '%s %.2f' % (names[int(cls)], conf)
                if names[int(cls)]  in ["cat","dog","person"]:
                    print("find a ",names[int(cls)]," pass!!!")
                    # plot_one_box(xyxy, depth_colormap, label=label, color=colors[int(cls)])
                    plot_one_box(xyxy, frame, label=label, color=colors[int(cls)])
                    # print(xyxy)
                    midx, midy = int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)
                    # 获取中心的深度
                    info2 = "demo"
                    plot_info(frame, midx, midy + 15, info2)

        cv2.imshow("video", frame)
        key = cv2.waitKey(50)
        #print(key)
        if key  == ord('q'):  #判断是哪一个键按下
            break
    cv2.destroyAllWindows()
