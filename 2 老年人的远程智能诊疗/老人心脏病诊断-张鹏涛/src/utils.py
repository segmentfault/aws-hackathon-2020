import pandas as pd
import numpy as np


def read_data(data_file, data_columns=None):
    """
    :param data_file:  要读出的数据
    :param data_columns: 要读取的数据特征名称
    :return:  经过处理后的特征值以及标签值
    """
    data = pd.read_csv(data_file)
    data.columns = data_columns

    label = data.iloc[:, -1]
    feat = data.iloc[:, :-1]
    # 对数据进行缺失值的填充
    feat = feat.fillna(0)

    return feat, label
