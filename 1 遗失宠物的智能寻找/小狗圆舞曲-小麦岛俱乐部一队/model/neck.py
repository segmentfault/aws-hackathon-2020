import paddle.fluid.layers as L

from model.custom_layers import Conv2dUnit



class FPN(object):
    def __init__(self,
                 num_chan=256,
                 use_p6p7=True,
                 in_chs=[2048, 1024, 512]):
        super(FPN, self).__init__()
        self.use_p6p7 = use_p6p7

        # 对骨干网络的sxx进行卷积
        self.s32_conv = Conv2dUnit(in_chs[0], num_chan, 1, stride=1, bias_attr=True, act=None, name='fpn.s32_conv')
        self.s16_conv = Conv2dUnit(in_chs[1], num_chan, 1, stride=1, bias_attr=True, act=None, name='fpn.s16_conv')
        self.s8_conv = Conv2dUnit(in_chs[2], num_chan, 1, stride=1, bias_attr=True, act=None, name='fpn.s8_conv')
        self.convs = [self.s32_conv, self.s16_conv, self.s8_conv]

        # 第二次卷积
        self.sc_s32_conv = Conv2dUnit(num_chan, num_chan, 3, stride=1, bias_attr=True, act=None, name='fpn.sc_s32_conv')
        self.sc_s16_conv = Conv2dUnit(num_chan, num_chan, 3, stride=1, bias_attr=True, act=None, name='fpn.sc_s16_conv')
        self.sc_s8_conv = Conv2dUnit(num_chan, num_chan, 3, stride=1, bias_attr=True, act=None, name='fpn.sc_s8_conv')
        self.second_convs = [self.sc_s32_conv, self.sc_s16_conv, self.sc_s8_conv]

        # p6p7
        if self.use_p6p7:
            self.p6_conv = Conv2dUnit(num_chan, num_chan, 3, stride=2, bias_attr=True, act=None, name='fpn.p6_conv')
            self.p7_conv = Conv2dUnit(num_chan, num_chan, 3, stride=2, bias_attr=True, act=None, name='fpn.p7_conv')

    def __call__(self, body_feats):
        '''
        :param body_feats:  [s8, s16, s32]
        :return:
                                     bs32
                                      |
                                     卷积
                                      |
                             bs16   [fs32]
                              |       |
                            卷积    上采样
                              |       |
                          lateral   topdown
                               \    /
                                相加
                                  |
                        bs8     [fs16]
                         |        |
                        卷积    上采样
                         |        |
                      lateral   topdown
                            \    /
                             相加
                               |
                             [fs8]

                fpn_inner_output = [fs32, fs16, fs8]
        然后  fs32, fs16, fs8  分别再接一个卷积得到 p5, p4, p3 ；
        p5 接一个卷积得到 p6， p6 接一个卷积得到 p7。
        '''
        reverse_body_feats = body_feats[::-1]   #   [s32, s16, s8]

        num_backbone_stages = len(reverse_body_feats)   # 3
        # fpn内部的输出
        fpn_inner_output = [None for _ in range(num_backbone_stages)]

        body_input = reverse_body_feats[0]   # 骨干网络的s32。先接一个卷积
        fpn_inner_output[0] = self.convs[0](body_input)   # fpn的s32
        for i in range(1, num_backbone_stages):
            body_input = reverse_body_feats[i]     # 骨干网络的s16
            top_output = fpn_inner_output[i - 1]   # fpn的s32

            # 骨干网络的s16卷积，fpn的s32上采样，再融合，融合方式为逐元素相加
            lateral = self.convs[i](body_input)   # 骨干网络的s16卷积，stride=16
            topdown = L.resize_nearest(top_output, scale=float(2))   # fpn的s32上采样，stride=16
            fpn_inner_single = lateral + topdown   # fpn的s16
            fpn_inner_output[i] = fpn_inner_single   # fpn的s16


        # 第二次卷积
        fpn_outputs = [None for _ in range(num_backbone_stages)]
        for i in range(num_backbone_stages):
            fpn_input = fpn_inner_output[i]   # fpn的s32
            fpn_output = self.second_convs[i](fpn_input)   # fpn的s32
            fpn_outputs[i] = fpn_output

        # p6p7
        if self.use_p6p7:
            p6_input = fpn_outputs[0]   # p5
            p6 = self.p6_conv(p6_input)
            p7 = self.p7_conv(p6)
            outs = [p7, p6] + fpn_outputs   # [p7, p6, p5, p4, p3]
            spatial_scale = [1. / 128., 1. / 64., 1. / 32., 1. / 16., 1. / 8.]
            return outs, spatial_scale
        else:
            outs = fpn_outputs   # [p5, p4, p3]
            spatial_scale = [1. / 32., 1. / 16., 1. / 8.]
            return outs, spatial_scale
