import paddle.fluid.layers as L

from model.custom_layers import Conv2dUnit


class ConvBlock(object):
    def __init__(self, in_c, filters, bn, gn, af, use_dcn=False, stride=2, downsample_in3x3=True, block_name=''):
        '''
        ResNetVB的下采样是在中间的3x3卷积层进行。
        '''
        super(ConvBlock, self).__init__()
        filters1, filters2, filters3 = filters
        if downsample_in3x3 == True:
            stride1, stride2 = 1, stride
        else:
            stride1, stride2 = stride, 1

        self.conv1 = Conv2dUnit(in_c, filters1, 1, stride=stride1, bn=bn, gn=gn, af=af, act='relu',
                                name=block_name + '.conv0')
        self.conv2 = Conv2dUnit(filters1, filters2, 3, stride=stride2, bn=bn, gn=gn, af=af, act='relu', use_dcn=use_dcn,
                                name=block_name + '.conv1')
        self.conv3 = Conv2dUnit(filters2, filters3, 1, stride=1, bn=bn, gn=gn, af=af, act=None,
                                name=block_name + '.conv2')

        self.conv4 = Conv2dUnit(in_c, filters3, 1, stride=stride, bn=bn, gn=gn, af=af, act=None,
                                name=block_name + '.conv3')

    def __call__(self, input_tensor):
        x = self.conv1(input_tensor)
        x = self.conv2(x)
        x = self.conv3(x)
        shortcut = self.conv4(input_tensor)
        x = L.elementwise_add(x=x, y=shortcut, act=None)
        x = L.relu(x)
        return x


class IdentityBlock(object):
    def __init__(self, in_c, filters, bn, gn, af, use_dcn=False, block_name=''):
        super(IdentityBlock, self).__init__()
        filters1, filters2, filters3 = filters

        self.conv1 = Conv2dUnit(in_c, filters1, 1, stride=1, bn=bn, gn=gn, af=af, act='relu',
                                name=block_name + '.conv0')
        self.conv2 = Conv2dUnit(filters1, filters2, 3, stride=1, bn=bn, gn=gn, af=af, act='relu', use_dcn=use_dcn,
                                name=block_name + '.conv1')
        self.conv3 = Conv2dUnit(filters2, filters3, 1, stride=1, bn=bn, gn=gn, af=af, act=None,
                                name=block_name + '.conv2')

    def __call__(self, input_tensor):
        x = self.conv1(input_tensor)
        x = self.conv2(x)
        x = self.conv3(x)
        x = L.elementwise_add(x=x, y=input_tensor, act=None)
        x = L.relu(x)
        return x


class Resnet(object):
    def __init__(self, depth, norm_type='affine_channel', feature_maps=[3, 4, 5], use_dcn=False, downsample_in3x3=True):
        super(Resnet, self).__init__()
        assert depth in [50, 101]
        self.depth = depth
        self.feature_maps = feature_maps
        self.use_dcn = use_dcn

        bn = 0
        gn = 0
        af = 0
        if norm_type == 'bn':
            bn = 1
        elif norm_type == 'gn':
            gn = 1
        elif norm_type == 'affine_channel':
            af = 1
        self.conv1 = Conv2dUnit(3, 64, 7, stride=2, bn=bn, gn=gn, af=af, act='relu', name='backbone.stage1.0.conv0')

        # stage2
        self.stage2_0 = ConvBlock(64, [64, 64, 256], bn, gn, af, stride=1, downsample_in3x3=downsample_in3x3,
                                  block_name='backbone.stage2.0')
        self.stage2_1 = IdentityBlock(256, [64, 64, 256], bn, gn, af, block_name='backbone.stage2.1')
        self.stage2_2 = IdentityBlock(256, [64, 64, 256], bn, gn, af, block_name='backbone.stage2.2')

        # stage3
        self.stage3_0 = ConvBlock(256, [128, 128, 512], bn, gn, af, use_dcn=use_dcn, downsample_in3x3=downsample_in3x3,
                                  block_name='backbone.stage3.0')
        self.stage3_1 = IdentityBlock(512, [128, 128, 512], bn, gn, af, use_dcn=use_dcn, block_name='backbone.stage3.1')
        self.stage3_2 = IdentityBlock(512, [128, 128, 512], bn, gn, af, use_dcn=use_dcn, block_name='backbone.stage3.2')
        self.stage3_3 = IdentityBlock(512, [128, 128, 512], bn, gn, af, use_dcn=use_dcn, block_name='backbone.stage3.3')

        # stage4
        self.stage4_0 = ConvBlock(512, [256, 256, 1024], bn, gn, af, use_dcn=use_dcn, downsample_in3x3=downsample_in3x3,
                                  block_name='backbone.stage4.0')
        k = 21
        if depth == 50:
            k = 4
        self.stage4_layers = []
        p = 1
        for i in range(k):
            ly = IdentityBlock(1024, [256, 256, 1024], bn, gn, af, use_dcn=use_dcn, block_name='backbone.stage4.%d' % p)
            self.stage4_layers.append(ly)
            p += 1
        self.stage4_last_layer = IdentityBlock(1024, [256, 256, 1024], bn, gn, af, use_dcn=use_dcn,
                                               block_name='backbone.stage4.%d' % p)

        # stage5
        self.stage5_0 = ConvBlock(1024, [512, 512, 2048], bn, gn, af, use_dcn=use_dcn,
                                  downsample_in3x3=downsample_in3x3, block_name='backbone.stage5.0')
        self.stage5_1 = IdentityBlock(2048, [512, 512, 2048], bn, gn, af, use_dcn=use_dcn,
                                      block_name='backbone.stage5.1')
        self.stage5_2 = IdentityBlock(2048, [512, 512, 2048], bn, gn, af, use_dcn=use_dcn,
                                      block_name='backbone.stage5.2')

    def __call__(self, input_tensor):
        x = self.conv1(input_tensor)
        x = L.pool2d(
            input=x,
            pool_size=3,
            pool_stride=2,
            pool_padding=1,
            pool_type='max')

        # stage2
        x = self.stage2_0(x)
        x = self.stage2_1(x)
        s4 = self.stage2_2(x)
        # stage3
        x = self.stage3_0(s4)
        x = self.stage3_1(x)
        x = self.stage3_2(x)
        s8 = self.stage3_3(x)
        # stage4
        x = self.stage4_0(s8)
        for ly in self.stage4_layers:
            x = ly(x)
        s16 = self.stage4_last_layer(x)
        # stage5
        x = self.stage5_0(s16)
        x = self.stage5_1(x)
        s32 = self.stage5_2(x)

        outs = []
        if 2 in self.feature_maps:
            outs.append(s4)
        if 3 in self.feature_maps:
            outs.append(s8)
        if 4 in self.feature_maps:
            outs.append(s16)
        if 5 in self.feature_maps:
            outs.append(s32)
        return outs
