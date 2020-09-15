import paddle.fluid as fluid
from paddle.fluid.param_attr import ParamAttr
from paddle.fluid.regularizer import L2Decay
from paddle.fluid.initializer import Constant


class Conv2dUnit(object):
    def __init__(self,
                 input_dim,
                 filters,
                 filter_size,
                 stride=1,
                 bias_attr=False,
                 bn=0,
                 gn=0,
                 af=0,
                 groups=32,
                 act=None,
                 freeze_norm=False,
                 is_test=False,
                 norm_decay=0.,
                 use_dcn=False,
                 bias_init_value=None,
                 name=''):
        super(Conv2dUnit, self).__init__()
        self.input_dim = input_dim
        self.filters = filters
        self.filter_size = filter_size
        self.stride = stride
        self.bias_attr = bias_attr
        self.bn = bn
        self.gn = gn
        self.af = af
        self.groups = groups
        self.act = act
        self.freeze_norm = freeze_norm
        self.is_test = is_test
        self.norm_decay = norm_decay
        self.use_dcn = use_dcn
        self.bias_init_value = bias_init_value
        self.name = name

    def __call__(self, x):
        conv_name = self.name + ".conv"
        if self.use_dcn:
            pass
        else:
            battr = None
            if self.bias_attr:
                initializer = None
                if self.bias_init_value:
                    initializer = Constant(value=self.bias_init_value)
                battr = ParamAttr(name=conv_name + ".bias", initializer=initializer)
            x = fluid.layers.conv2d(
                input=x,
                num_filters=self.filters,
                filter_size=self.filter_size,
                stride=self.stride,
                padding=(self.filter_size - 1) // 2,
                act=None,
                param_attr=ParamAttr(name=conv_name + ".weight"),
                bias_attr=battr,
                name=conv_name + '.output.1')
        if self.bn:
            bn_name = self.name + ".bn"
            norm_lr = 0. if self.freeze_norm else 1.  # 归一化层学习率
            norm_decay = self.norm_decay  # 衰减
            pattr = ParamAttr(
                name=bn_name + '.scale',
                learning_rate=norm_lr,
                regularizer=L2Decay(norm_decay))  # L2权重衰减正则化
            battr = ParamAttr(
                name=bn_name + '.offset',
                learning_rate=norm_lr,
                regularizer=L2Decay(norm_decay))  # L2权重衰减正则化
            x = fluid.layers.batch_norm(
                input=x,
                name=bn_name + '.output.1',
                is_test=self.is_test,  # 冻结层时（即trainable=False），bn的均值、标准差也还是会变化，只有设置is_test=True才保证不变
                param_attr=pattr,
                bias_attr=battr,
                moving_mean_name=bn_name + '.mean',
                moving_variance_name=bn_name + '.var')
        if self.gn:
            gn_name = self.name + ".gn"
            norm_lr = 0. if self.freeze_norm else 1.  # 归一化层学习率
            norm_decay = self.norm_decay  # 衰减
            pattr = ParamAttr(
                name=gn_name + '.scale',
                learning_rate=norm_lr,
                regularizer=L2Decay(norm_decay))  # L2权重衰减正则化
            battr = ParamAttr(
                name=gn_name + '.offset',
                learning_rate=norm_lr,
                regularizer=L2Decay(norm_decay))  # L2权重衰减正则化
            x = fluid.layers.group_norm(
                input=x,
                groups=self.groups,
                name=gn_name + '.output.1',
                param_attr=pattr,
                bias_attr=battr)
        if self.af:
            af_name = self.name + ".af"
            norm_lr = 0. if self.freeze_norm else 1.  # 归一化层学习率
            norm_decay = self.norm_decay  # 衰减
            pattr = ParamAttr(
                name=af_name + '.scale',
                learning_rate=norm_lr,
                regularizer=L2Decay(norm_decay))  # L2权重衰减正则化
            battr = ParamAttr(
                name=af_name + '.offset',
                learning_rate=norm_lr,
                regularizer=L2Decay(norm_decay))  # L2权重衰减正则化
            scale = fluid.layers.create_parameter(
                shape=[x.shape[1]],
                dtype=x.dtype,
                attr=pattr,
                default_initializer=fluid.initializer.Constant(1.))
            bias = fluid.layers.create_parameter(
                shape=[x.shape[1]],
                dtype=x.dtype,
                attr=battr,
                default_initializer=fluid.initializer.Constant(0.))
            x = fluid.layers.affine_channel(x, scale=scale, bias=bias)
        if self.act == 'leaky':
            x = fluid.layers.leaky_relu(x, alpha=0.1)
        elif self.act == 'relu':
            x = fluid.layers.relu(x)
        return x
