import numpy as np
import math

from paddle import fluid
import paddle.fluid.layers as L

from model.custom_layers import Conv2dUnit


class FCOSHead(object):
    def __init__(self,
                 num_classes,
                 fpn_stride=[8, 16, 32, 64, 128],
                 prior_prob=0.01,
                 num_convs=4,
                 batch_size=1,
                 norm_type="gn",
                 fcos_loss=None,
                 norm_reg_targets=True,
                 centerness_on_reg=True,
                 use_dcn_in_tower=False,
                 nms_cfg=None
                 ):
        super(FCOSHead, self).__init__()
        self.num_classes = num_classes
        self.fpn_stride = fpn_stride[::-1]
        self.prior_prob = prior_prob
        self.num_convs = num_convs
        self.norm_reg_targets = norm_reg_targets
        self.centerness_on_reg = centerness_on_reg
        self.use_dcn_in_tower = use_dcn_in_tower
        self.norm_type = norm_type
        self.fcos_loss = fcos_loss
        self.batch_size = batch_size
        self.nms_cfg = nms_cfg


        self.scales_on_reg = []       # 回归分支（预测框坐标）的系数
        self.cls_convs_per_feature = []   # 每个fpn输出特征图再进行卷积的卷积层，用于预测类别
        self.reg_convs_per_feature = []   # 每个fpn输出特征图再进行卷积的卷积层，用于预测坐标
        self.ctn_convs_per_feature = []   # 用于预测centerness
        n = len(self.fpn_stride)      # 有n个输出层
        for i in range(n):     # 遍历每个输出层
            scale = fluid.layers.create_parameter(
                shape=[1, ],
                dtype="float32",
                name="head.scale_%d" % i,
                default_initializer=fluid.initializer.Constant(1.))
            self.scales_on_reg.append(scale)
            cls_convs_this_feature = []   # 这个fpn输出特征图再进行卷积的卷积层，用于预测类别
            reg_convs_this_feature = []   # 这个fpn输出特征图再进行卷积的卷积层，用于预测坐标
            for lvl in range(0, self.num_convs):
                # 使用gn，组数是32，而且带激活relu
                cls_conv_layer = Conv2dUnit(256, 256, 3, stride=1, bias_attr=True, gn=1, groups=32, act='relu', name='head.cls_convs_per_feature.%d.%d' % (i, lvl))
                cls_convs_this_feature.append(cls_conv_layer)
                reg_conv_layer = Conv2dUnit(256, 256, 3, stride=1, bias_attr=True, gn=1, groups=32, act='relu', name='head.reg_convs_per_feature.%d.%d' % (i, lvl))
                reg_convs_this_feature.append(reg_conv_layer)

            # 类别分支最后的卷积。设置偏移的初始值使得各类别预测概率初始值为self.prior_prob (根据激活函数是sigmoid()时推导出，和RetinaNet中一样)
            bias_init_value = -math.log((1 - self.prior_prob) / self.prior_prob)
            cls_last_conv_layer = Conv2dUnit(256, self.num_classes, 3, stride=1, bias_attr=True, act=None, bias_init_value=bias_init_value, name='head.cls_convs_per_feature.%d.%d' % (i, self.num_convs))
            # 坐标分支最后的卷积
            reg_last_conv_layer = Conv2dUnit(256, 4, 3, stride=1, bias_attr=True, act=None, name='head.reg_convs_per_feature.%d.%d' % (i, self.num_convs))
            # centerness分支
            ctn_last_conv_layer = Conv2dUnit(256, 1, 3, stride=1, bias_attr=True, act=None, name='head.ctn_convs_per_feature.%d' % (i, ))

            cls_convs_this_feature.append(cls_last_conv_layer)
            reg_convs_this_feature.append(reg_last_conv_layer)
            self.cls_convs_per_feature.append(cls_convs_this_feature)
            self.reg_convs_per_feature.append(reg_convs_this_feature)
            self.ctn_convs_per_feature.append(ctn_last_conv_layer)

    def _fcos_head(self, features, fpn_stride, i, is_training=False):
        """
        Args:
            features (Variables): feature map from FPN
            fpn_stride     (int): the stride of current feature map
            is_training   (bool): whether is train or test mode
        """
        fpn_scale = self.scales_on_reg[i]
        subnet_blob_cls = features
        subnet_blob_reg = features
        # if self.use_dcn_in_tower:
        #     conv_norm = DeformConvNorm
        # else:
        #     conv_norm = ConvNorm
        for lvl in range(0, self.num_convs):
            subnet_blob_cls = self.cls_convs_per_feature[i][lvl](subnet_blob_cls)
            subnet_blob_reg = self.reg_convs_per_feature[i][lvl](subnet_blob_reg)


        cls_logits = self.cls_convs_per_feature[i][-1](subnet_blob_cls)   # 通道数变成类别数
        bbox_reg = self.reg_convs_per_feature[i][-1](subnet_blob_reg)     # 通道数变成4
        bbox_reg = bbox_reg * fpn_scale     # 预测坐标的特征图整体乘上fpn_scale，是一个可学习参数
        # 如果 归一化坐标分支，bbox_reg进行relu激活
        if self.norm_reg_targets:
            bbox_reg = fluid.layers.relu(bbox_reg)
            if not is_training:   # 验证状态的话，bbox_reg再乘以下采样倍率
                bbox_reg = bbox_reg * fpn_stride
        else:
            bbox_reg = fluid.layers.exp(bbox_reg)


        # ============= centerness分支，默认是用坐标分支接4个卷积层之后的结果subnet_blob_reg =============
        if self.centerness_on_reg:
            centerness = self.ctn_convs_per_feature[i](subnet_blob_reg)
        else:
            centerness = self.ctn_convs_per_feature[i](subnet_blob_cls)
        return cls_logits, bbox_reg, centerness

    def _get_output(self, body_feats, is_training=False):
        """
        Args:
            body_feates (list): the list of fpn feature maps
            is_training (bool): whether is train or test mode
        Return:
            cls_logits (Variables): prediction for classification
            bboxes_reg (Variables): prediction for bounding box
            centerness (Variables): prediction for ceterness
        """
        cls_logits = []
        bboxes_reg = []
        centerness = []
        assert len(body_feats) == len(self.fpn_stride), \
            "The size of body_feats is not equal to size of fpn_stride"
        i = 0
        for features, fpn_stride in zip(body_feats, self.fpn_stride):
            cls_pred, bbox_pred, ctn_pred = self._fcos_head(
                features, fpn_stride, i, is_training=is_training)
            cls_logits.append(cls_pred)
            bboxes_reg.append(bbox_pred)
            centerness.append(ctn_pred)
            i += 1
        return cls_logits, bboxes_reg, centerness

    def _compute_locations(self, features):
        """
        Args:
            features (list): List of Variables for FPN feature maps
        Return:
            Anchor points for each feature map pixel
        """
        locations = []
        for lvl, feature in enumerate(features):
            shape_fm = fluid.layers.shape(feature)
            shape_fm.stop_gradient = True
            h = shape_fm[2]
            w = shape_fm[3]
            fpn_stride = self.fpn_stride[lvl]
            shift_x = fluid.layers.range(
                0, w * fpn_stride, fpn_stride, dtype='float32')
            shift_y = fluid.layers.range(
                0, h * fpn_stride, fpn_stride, dtype='float32')
            shift_x = fluid.layers.unsqueeze(shift_x, axes=[0])
            shift_y = fluid.layers.unsqueeze(shift_y, axes=[1])
            shift_x = fluid.layers.expand_as(
                shift_x, target_tensor=feature[0, 0, :, :])
            shift_y = fluid.layers.expand_as(
                shift_y, target_tensor=feature[0, 0, :, :])
            shift_x.stop_gradient = True
            shift_y.stop_gradient = True
            shift_x = fluid.layers.reshape(shift_x, shape=[-1])
            shift_y = fluid.layers.reshape(shift_y, shape=[-1])
            location = fluid.layers.stack(
                [shift_x, shift_y], axis=-1) + fpn_stride // 2        # [h*w, 2]  格子中心点的坐标，单位是1像素。顺序是先第一行格子从左到右，再到第二行格子从左到右，...
            location.stop_gradient = True
            locations.append(location)
        return locations

    def __merge_hw(self, input, ch_type="channel_first"):
        """
        Args:
            input (Variables): Feature map whose H and W will be merged into one dimension
            ch_type     (str): channel_first / channel_last
        Return:
            new_shape (Variables): The new shape after h and w merged into one dimension
        """
        shape_ = fluid.layers.shape(input)
        bs = shape_[0]
        ch = shape_[1]
        hi = shape_[2]
        wi = shape_[3]
        img_size = hi * wi
        img_size.stop_gradient = True
        if ch_type == "channel_first":
            new_shape = fluid.layers.concat([bs, ch, img_size])
        elif ch_type == "channel_last":
            new_shape = fluid.layers.concat([bs, img_size, ch])
        else:
            raise KeyError("Wrong ch_type %s" % ch_type)
        new_shape.stop_gradient = True
        return new_shape

    def _postprocessing_by_level(self, locations, box_cls, box_reg, box_ctn,
                                 im_info):
        """
        Args:
            locations (Variables): anchor points for current layer
            box_cls   (Variables): categories prediction
            box_reg   (Variables): bounding box prediction
            box_ctn   (Variables): centerness prediction
            im_info   (Variables): [h, w, scale] for input images
        Return:
            box_cls_ch_last  (Variables): score for each category, in [N, C, M]
                C is the number of classes and M is the number of anchor points
            box_reg_decoding (Variables): decoded bounding box, in [N, M, 4]
                last dimension is [x1, y1, x2, y2]
        """
        # =========== 类别概率，[N, 80, H*W] ===========
        act_shape_cls = self.__merge_hw(box_cls)
        box_cls_ch_last = fluid.layers.reshape(
            x=box_cls,
            shape=[self.batch_size, self.num_classes, -1],
            actual_shape=act_shape_cls)
        box_cls_ch_last = fluid.layers.sigmoid(box_cls_ch_last)  # 类别概率用sigmoid()激活，[N, 80, H*W]

        # =========== 坐标(4个偏移)，[N, H*W, 4] ===========
        act_shape_reg = self.__merge_hw(box_reg, "channel_last")
        box_reg_ch_last = fluid.layers.transpose(box_reg, perm=[0, 2, 3, 1])
        box_reg_ch_last = fluid.layers.reshape(
            x=box_reg_ch_last,
            shape=[self.batch_size, -1, 4],
            actual_shape=act_shape_reg)   # [N, H*W, 4]，坐标不用再接激活层，直接预测。

        # =========== centerness，[N, 1, H*W] ===========
        act_shape_ctn = self.__merge_hw(box_ctn)
        box_ctn_ch_last = fluid.layers.reshape(
            x=box_ctn,
            shape=[self.batch_size, 1, -1],
            actual_shape=act_shape_ctn)
        box_ctn_ch_last = fluid.layers.sigmoid(box_ctn_ch_last)  # centerness用sigmoid()激活，[N, 1, H*W]

        box_reg_decoding = fluid.layers.stack(
            [
                locations[:, 0] - box_reg_ch_last[:, :, 0],
                locations[:, 1] - box_reg_ch_last[:, :, 1],
                locations[:, 0] + box_reg_ch_last[:, :, 2],
                locations[:, 1] + box_reg_ch_last[:, :, 3]
            ],
            axis=1)
        box_reg_decoding = fluid.layers.transpose(
            box_reg_decoding, perm=[0, 2, 1])
        # recover the location to original image
        im_scale = im_info[:, 2]
        box_reg_decoding = box_reg_decoding / im_scale  # [N, H*W, 4]，最终坐标=坐标*图片缩放因子
        box_cls_ch_last = box_cls_ch_last * box_ctn_ch_last  # [N, 80, H*W]，最终分数=类别概率*centerness
        return box_cls_ch_last, box_reg_decoding

    def _post_processing(self, locations, cls_logits, bboxes_reg, centerness,
                         im_info):
        """
        Args:
            locations   (list): List of Variables composed by center of each anchor point
            cls_logits  (list): List of Variables for class prediction
            bboxes_reg  (list): List of Variables for bounding box prediction
            centerness  (list): List of Variables for centerness prediction
            im_info(Variables): [h, w, scale] for input images
        Return:
            pred (LoDTensor): predicted bounding box after nms,
                the shape is n x 6, last dimension is [label, score, xmin, ymin, xmax, ymax]
        """
        pred_boxes_ = []
        pred_scores_ = []
        for _, (
                pts, cls, box, ctn
        ) in enumerate(zip(locations, cls_logits, bboxes_reg, centerness)):
            pred_scores_lvl, pred_boxes_lvl = self._postprocessing_by_level(
                pts, cls, box, ctn, im_info)
            pred_boxes_.append(pred_boxes_lvl)     # [N, H*W, 4]，最终坐标
            pred_scores_.append(pred_scores_lvl)   # [N, 80, H*W]，最终分数
        pred_boxes = fluid.layers.concat(pred_boxes_, axis=1)    # [N, 所有格子, 4]，最终坐标
        pred_scores = fluid.layers.concat(pred_scores_, axis=2)  # [N, 80, 所有格子]，最终分数

        # nms
        pred = None
        nms_type = self.nms_cfg['nms_type']
        if nms_type == 'multiclass_nms':
            pred = fluid.layers.multiclass_nms(pred_boxes, pred_scores,
                                               score_threshold=self.nms_cfg['conf_thresh'],
                                               nms_top_k=self.nms_cfg['nms_top_k'],
                                               keep_top_k=self.nms_cfg['keep_top_k'],
                                               nms_threshold=self.nms_cfg['nms_thresh'],
                                               background_label=-1)  # 一定要设置background_label=-1，否则检测不出人。
        return pred

    def get_loss(self, input, tag_labels, tag_bboxes, tag_centerness):
        """
        Calculate the loss for FCOS
        Args:
            input           (list): List of Variables for feature maps from FPN layers
            tag_labels     (Variables): category targets for each anchor point
            tag_bboxes     (Variables): bounding boxes  targets for positive samples
            tag_centerness (Variables): centerness targets for positive samples
        Return:
            loss (dict): loss composed by classification loss, bounding box
                regression loss and centerness regression loss
        """
        cls_logits, bboxes_reg, centerness = self._get_output(
            input, is_training=True)
        loss = self.fcos_loss(cls_logits, bboxes_reg, centerness, tag_labels,
                              tag_bboxes, tag_centerness)
        return loss

    def get_prediction(self, input, im_info):
        """
        Decode the prediction
        Args:
            input: [c7, c6, c5, c4, c3]
            im_info(Variables): [h, w, scale] for input images
        Return:
            the bounding box prediction
        """
        # cls_logits里面每个元素是[N, 80, 格子行数, 格子列数]
        # bboxes_reg里面每个元素是[N,  4, 格子行数, 格子列数]
        # centerness里面每个元素是[N,  1, 格子行数, 格子列数]
        cls_logits, bboxes_reg, centerness = self._get_output(
            input, is_training=False)
        locations = self._compute_locations(input)
        pred = self._post_processing(locations, cls_logits, bboxes_reg,
                                     centerness, im_info)
        # return {"bbox": pred}
        return pred



class FCOSSharedHead(object):
    def __init__(self,
                 num_classes,
                 fpn_stride=[8, 16, 32, 64, 128],
                 thresh_with_ctr=True,
                 prior_prob=0.01,
                 num_convs=4,
                 batch_size=1,
                 norm_type="gn",
                 fcos_loss=None,
                 norm_reg_targets=True,
                 centerness_on_reg=True,
                 use_dcn_in_tower=False,
                 nms_cfg=None
                 ):
        super(FCOSSharedHead, self).__init__()
        self.num_classes = num_classes
        self.fpn_stride = fpn_stride[::-1]
        self.thresh_with_ctr = thresh_with_ctr
        self.prior_prob = prior_prob
        self.num_convs = num_convs
        self.norm_reg_targets = norm_reg_targets
        self.centerness_on_reg = centerness_on_reg
        self.use_dcn_in_tower = use_dcn_in_tower
        self.norm_type = norm_type
        self.fcos_loss = fcos_loss
        self.batch_size = batch_size
        self.nms_cfg = nms_cfg


        self.scales_on_reg = []       # 回归分支（预测框坐标）的系数
        self.cls_convs = []   # 每个fpn输出特征图  共享的  再进行卷积的卷积层，用于预测类别
        self.reg_convs = []   # 每个fpn输出特征图  共享的  再进行卷积的卷积层，用于预测坐标
        self.ctn_conv = Conv2dUnit(256, 1, 3, stride=1, bias_attr=True, act=None, name='head.ctn_conv')   # 用于预测centerness

        # 每个fpn输出特征图  共享的  卷积层。
        for lvl in range(0, self.num_convs):
            # 使用gn，组数是32，而且带激活relu
            cls_conv_layer = Conv2dUnit(256, 256, 3, stride=1, bias_attr=True, gn=1, groups=32, act='relu', name='head.cls_convs.%d' % (lvl, ))
            self.cls_convs.append(cls_conv_layer)
            reg_conv_layer = Conv2dUnit(256, 256, 3, stride=1, bias_attr=True, gn=1, groups=32, act='relu', name='head.reg_convs.%d' % (lvl, ))
            self.reg_convs.append(reg_conv_layer)
        # 类别分支最后的卷积。设置偏移的初始值使得各类别预测概率初始值为self.prior_prob (根据激活函数是sigmoid()时推导出，和RetinaNet中一样)
        bias_init_value = -math.log((1 - self.prior_prob) / self.prior_prob)
        cls_last_conv_layer = Conv2dUnit(256, self.num_classes, 3, stride=1, bias_attr=True, act=None, bias_init_value=bias_init_value, name='head.cls_convs.%d' % (self.num_convs, ))
        # 坐标分支最后的卷积
        reg_last_conv_layer = Conv2dUnit(256, 4, 3, stride=1, bias_attr=True, act=None, name='head.reg_convs.%d' % (self.num_convs, ))
        self.cls_convs.append(cls_last_conv_layer)
        self.reg_convs.append(reg_last_conv_layer)


        n = len(self.fpn_stride)      # 有n个输出层
        for i in range(n):     # 遍历每个输出层
            scale = fluid.layers.create_parameter(
                shape=[1, ],
                dtype="float32",
                name="head.scale_%d" % i,
                default_initializer=fluid.initializer.Constant(1.))
            self.scales_on_reg.append(scale)

    def _fcos_head(self, features, fpn_stride, i, is_training=False):
        """
        Args:
            features (Variables): feature map from FPN
            fpn_stride     (int): the stride of current feature map
            is_training   (bool): whether is train or test mode
        """
        fpn_scale = self.scales_on_reg[i]
        subnet_blob_cls = features
        subnet_blob_reg = features
        # if self.use_dcn_in_tower:
        #     conv_norm = DeformConvNorm
        # else:
        #     conv_norm = ConvNorm
        for lvl in range(0, self.num_convs):
            subnet_blob_cls = self.cls_convs[lvl](subnet_blob_cls)
            subnet_blob_reg = self.reg_convs[lvl](subnet_blob_reg)


        cls_logits = self.cls_convs[-1](subnet_blob_cls)   # 通道数变成类别数
        bbox_reg = self.reg_convs[-1](subnet_blob_reg)     # 通道数变成4
        bbox_reg = bbox_reg * fpn_scale     # 预测坐标的特征图整体乘上fpn_scale，是一个可学习参数
        # 如果 归一化坐标分支，bbox_reg进行relu激活
        if self.norm_reg_targets:
            bbox_reg = fluid.layers.relu(bbox_reg)
            if not is_training:   # 验证状态的话，bbox_reg再乘以下采样倍率
                bbox_reg = bbox_reg * fpn_stride
        else:
            bbox_reg = fluid.layers.exp(bbox_reg)


        # ============= centerness分支，默认是用坐标分支接4个卷积层之后的结果subnet_blob_reg =============
        if self.centerness_on_reg:
            centerness = self.ctn_conv(subnet_blob_reg)
        else:
            centerness = self.ctn_conv(subnet_blob_cls)
        return cls_logits, bbox_reg, centerness

    def _get_output(self, body_feats, is_training=False):
        """
        Args:
            body_feates (list): the list of fpn feature maps
            is_training (bool): whether is train or test mode
        Return:
            cls_logits (Variables): prediction for classification
            bboxes_reg (Variables): prediction for bounding box
            centerness (Variables): prediction for ceterness
        """
        cls_logits = []
        bboxes_reg = []
        centerness = []
        assert len(body_feats) == len(self.fpn_stride), \
            "The size of body_feats is not equal to size of fpn_stride"
        i = 0
        for features, fpn_stride in zip(body_feats, self.fpn_stride):
            cls_pred, bbox_pred, ctn_pred = self._fcos_head(
                features, fpn_stride, i, is_training=is_training)
            cls_logits.append(cls_pred)
            bboxes_reg.append(bbox_pred)
            centerness.append(ctn_pred)
            i += 1
        return cls_logits, bboxes_reg, centerness

    def _compute_locations(self, features):
        """
        Args:
            features (list): List of Variables for FPN feature maps
        Return:
            Anchor points for each feature map pixel
        """
        locations = []
        for lvl, feature in enumerate(features):
            shape_fm = fluid.layers.shape(feature)
            shape_fm.stop_gradient = True
            h = shape_fm[2]
            w = shape_fm[3]
            fpn_stride = self.fpn_stride[lvl]
            shift_x = fluid.layers.range(
                0, w * fpn_stride, fpn_stride, dtype='float32')
            shift_y = fluid.layers.range(
                0, h * fpn_stride, fpn_stride, dtype='float32')
            shift_x = fluid.layers.unsqueeze(shift_x, axes=[0])
            shift_y = fluid.layers.unsqueeze(shift_y, axes=[1])
            shift_x = fluid.layers.expand_as(
                shift_x, target_tensor=feature[0, 0, :, :])
            shift_y = fluid.layers.expand_as(
                shift_y, target_tensor=feature[0, 0, :, :])
            shift_x.stop_gradient = True
            shift_y.stop_gradient = True
            shift_x = fluid.layers.reshape(shift_x, shape=[-1])
            shift_y = fluid.layers.reshape(shift_y, shape=[-1])
            location = fluid.layers.stack(
                [shift_x, shift_y], axis=-1) + fpn_stride // 2        # [h*w, 2]  格子中心点的坐标，单位是1像素。顺序是先第一行格子从左到右，再到第二行格子从左到右，...
            location.stop_gradient = True
            locations.append(location)
        return locations

    def __merge_hw(self, input, ch_type="channel_first"):
        """
        Args:
            input (Variables): Feature map whose H and W will be merged into one dimension
            ch_type     (str): channel_first / channel_last
        Return:
            new_shape (Variables): The new shape after h and w merged into one dimension
        """
        shape_ = fluid.layers.shape(input)
        bs = shape_[0]
        ch = shape_[1]
        hi = shape_[2]
        wi = shape_[3]
        img_size = hi * wi
        img_size.stop_gradient = True
        if ch_type == "channel_first":
            new_shape = fluid.layers.concat([bs, ch, img_size])
        elif ch_type == "channel_last":
            new_shape = fluid.layers.concat([bs, img_size, ch])
        else:
            raise KeyError("Wrong ch_type %s" % ch_type)
        new_shape.stop_gradient = True
        return new_shape

    def _postprocessing_by_level(self, locations, box_cls, box_reg, box_ctn,
                                 im_info):
        """
        Args:
            locations (Variables): anchor points for current layer
            box_cls   (Variables): categories prediction
            box_reg   (Variables): bounding box prediction
            box_ctn   (Variables): centerness prediction
            im_info   (Variables): [h, w, scale] for input images
        Return:
            box_cls_ch_last  (Variables): score for each category, in [N, C, M]
                C is the number of classes and M is the number of anchor points
            box_reg_decoding (Variables): decoded bounding box, in [N, M, 4]
                last dimension is [x1, y1, x2, y2]
        """
        # =========== 类别概率，[N, 80, H*W] ===========
        act_shape_cls = self.__merge_hw(box_cls)
        box_cls_ch_last = fluid.layers.reshape(
            x=box_cls,
            shape=[self.batch_size, self.num_classes, -1],
            actual_shape=act_shape_cls)
        box_cls_ch_last = fluid.layers.sigmoid(box_cls_ch_last)  # 类别概率用sigmoid()激活，[N, 80, H*W]

        # =========== 坐标(4个偏移)，[N, H*W, 4] ===========
        act_shape_reg = self.__merge_hw(box_reg, "channel_last")
        box_reg_ch_last = fluid.layers.transpose(box_reg, perm=[0, 2, 3, 1])
        box_reg_ch_last = fluid.layers.reshape(
            x=box_reg_ch_last,
            shape=[self.batch_size, -1, 4],
            actual_shape=act_shape_reg)   # [N, H*W, 4]，坐标不用再接激活层，直接预测。

        # =========== centerness，[N, 1, H*W] ===========
        act_shape_ctn = self.__merge_hw(box_ctn)
        box_ctn_ch_last = fluid.layers.reshape(
            x=box_ctn,
            shape=[self.batch_size, 1, -1],
            actual_shape=act_shape_ctn)
        box_ctn_ch_last = fluid.layers.sigmoid(box_ctn_ch_last)  # centerness用sigmoid()激活，[N, 1, H*W]

        box_reg_decoding = fluid.layers.stack(
            [
                locations[:, 0] - box_reg_ch_last[:, :, 0],
                locations[:, 1] - box_reg_ch_last[:, :, 1],
                locations[:, 0] + box_reg_ch_last[:, :, 2],
                locations[:, 1] + box_reg_ch_last[:, :, 3]
            ],
            axis=1)
        box_reg_decoding = fluid.layers.transpose(
            box_reg_decoding, perm=[0, 2, 1])
        # recover the location to original image
        im_scale = im_info[:, 2]
        box_reg_decoding = box_reg_decoding / im_scale  # [N, H*W, 4]，最终坐标=坐标*图片缩放因子
        if self.thresh_with_ctr:
            box_cls_ch_last = box_cls_ch_last * box_ctn_ch_last  # [N, 80, H*W]，最终分数=类别概率*centerness
        return box_cls_ch_last, box_reg_decoding

    def _post_processing(self, locations, cls_logits, bboxes_reg, centerness,
                         im_info):
        """
        Args:
            locations   (list): List of Variables composed by center of each anchor point
            cls_logits  (list): List of Variables for class prediction
            bboxes_reg  (list): List of Variables for bounding box prediction
            centerness  (list): List of Variables for centerness prediction
            im_info(Variables): [h, w, scale] for input images
        Return:
            pred (LoDTensor): predicted bounding box after nms,
                the shape is n x 6, last dimension is [label, score, xmin, ymin, xmax, ymax]
        """
        pred_boxes_ = []
        pred_scores_ = []
        for _, (
                pts, cls, box, ctn
        ) in enumerate(zip(locations, cls_logits, bboxes_reg, centerness)):
            pred_scores_lvl, pred_boxes_lvl = self._postprocessing_by_level(
                pts, cls, box, ctn, im_info)
            pred_boxes_.append(pred_boxes_lvl)     # [N, H*W, 4]，最终坐标
            pred_scores_.append(pred_scores_lvl)   # [N, 80, H*W]，最终分数
        pred_boxes = fluid.layers.concat(pred_boxes_, axis=1)    # [N, 所有格子, 4]，最终坐标
        pred_scores = fluid.layers.concat(pred_scores_, axis=2)  # [N, 80, 所有格子]，最终分数

        # nms
        pred = None
        nms_type = self.nms_cfg['nms_type']
        if nms_type == 'multiclass_nms':
            pred = fluid.layers.multiclass_nms(pred_boxes, pred_scores,
                                               score_threshold=self.nms_cfg['conf_thresh'],
                                               nms_top_k=self.nms_cfg['nms_top_k'],
                                               keep_top_k=self.nms_cfg['keep_top_k'],
                                               nms_threshold=self.nms_cfg['nms_thresh'],
                                               background_label=-1)  # 一定要设置background_label=-1，否则检测不出人。
        return pred

    def get_loss(self, input, tag_labels, tag_bboxes, tag_centerness):
        """
        Calculate the loss for FCOS
        Args:
            input           (list): List of Variables for feature maps from FPN layers
            tag_labels     (Variables): category targets for each anchor point
            tag_bboxes     (Variables): bounding boxes  targets for positive samples
            tag_centerness (Variables): centerness targets for positive samples
        Return:
            loss (dict): loss composed by classification loss, bounding box
                regression loss and centerness regression loss
        """
        cls_logits, bboxes_reg, centerness = self._get_output(
            input, is_training=True)
        loss = self.fcos_loss(cls_logits, bboxes_reg, centerness, tag_labels,
                              tag_bboxes, tag_centerness)
        return loss

    def get_prediction(self, input, im_info):
        """
        Decode the prediction
        Args:
            input: [c7, c6, c5, c4, c3]
            im_info(Variables): [h, w, scale] for input images
        Return:
            the bounding box prediction
        """
        # cls_logits里面每个元素是[N, 80, 格子行数, 格子列数]
        # bboxes_reg里面每个元素是[N,  4, 格子行数, 格子列数]
        # centerness里面每个元素是[N,  1, 格子行数, 格子列数]
        cls_logits, bboxes_reg, centerness = self._get_output(
            input, is_training=False)
        locations = self._compute_locations(input)
        pred = self._post_processing(locations, cls_logits, bboxes_reg,
                                     centerness, im_info)
        # return {"bbox": pred}
        return pred
