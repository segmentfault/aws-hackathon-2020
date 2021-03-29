import pandas as pd
import matplotlib as mpl
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt


data_file = "..\PRSA2017_Data_20130301-20170228\PRSA_Data_20130301-20170228\simpleDataSet.csv"
def build_lr():
    pd_data = pd.read_csv(data_file)

    X = pd_data.loc[:, ("PM10", "SO2","NO2","CO","PRES","DEWP")]
    y = pd_data.loc[:, "PM2.5"]
    
    #选择20%为测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=532) 

    print('训练集测试及参数:')
    print(f'X_train.shape={X_train.shape}\ny_train.shape ={y_train.shape}\nX_test.shape={X_test.shape}\ny_test.shape={y_test.shape}')

    linear_reg = LinearRegression()
    model = linear_reg.fit(X_train, y_train)

    print('模型参数')
    print(model)

    print('模型截距')
    print(linear_reg.intercept_)

    print('参数权重')
    print(linear_reg.coef_)

    y_pred = linear_reg.predict(X_test)
    sum_mean = 0

    for i in range(len(y_pred)):
        sum_mean += (y_pred[i] - y_test.values[i]) ** 2

    sum_erro = np.sqrt(sum_mean / len(y_pred))

    print(sum_erro)

    plt.figure()
    plt.figure()
    plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
    plt.plot(range(len(y_pred)), y_test, 'r', label="test")
    plt.legend(loc="upper right")
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()