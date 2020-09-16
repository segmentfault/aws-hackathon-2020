
from models import *  # set ONNX_EXPORT in models.py


def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = max(img1_shape) / max(img0_shape)  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    coords[:, [0, 2]] -= pad[0]  # x padding
    coords[:, [1, 3]] -= pad[1]  # y padding
    coords[:, :4] /= gain
    clip_coords(coords, img0_shape)
    return coords

def letterbox(img, new_shape=(416, 416), color=(128, 128, 128),
              auto=True, scaleFill=False, scaleup=True, interp=cv2.INTER_AREA):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = max(new_shape) / max(shape)
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 32), np.mod(dh, 32)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = new_shape
        ratio = new_shape[0] / shape[1], new_shape[1] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=interp)  # INTER_AREA is better, INTER_LINEAR is faster
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


class YOLO_Dectection:
    def __init__(self,device,cfg_path,weights_path,img_size=(416,416)):
        '''

        :param work_path:
        :param device:
        :param cfg_path:
        :param weights_path:

        '''
        self.device = device

        self.img_size = img_size
        self.model = Darknet(cfg_path, img_size)
        self.model.to(device).eval()
        if weights_path.endswith('.pt'):  # pytorch format
            self.model.load_state_dict(torch.load(weights_path, map_location=device)['model'])
        else:  # darknet format
            load_darknet_weights(self.model, weights_path)

    def detect(self,img):
        '''
        img:numpy.ndarray (h,w,channel)

        '''
        oral_size = img.shape
        # print(oral_size)
        img = letterbox(img, new_shape=self.img_size)[0]
        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device,dtype=torch.float32)
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference

        time_start = time.time()
        t1 = torch_utils.time_synchronized()
        pred = self.model(img)[0]
        t2 = torch_utils.time_synchronized()

        time_after_model = time.time()
        pred = non_max_suppression(pred,conf_thres=0.3, iou_thres=0.6, classes=None, agnostic=False)
        time_after_nms = time.time()

        # print("--model--time:",round(time_after_model-time_start,3),"s")
        # print("--nms--time:",round(time_after_nms-time_after_model,3),"s")

        det = pred[0]
        # print(det)
        if det is None:
            return None
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], oral_size).round()

        return det.cpu().detach().numpy()


