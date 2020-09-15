import pandas as pd
import matplotlib as mpl
import seaborn as sns

from matplotlib import pyplot as plt

# data_file = "..\PRSA2017_Data_20130301-20170228\PRSA_Data_20130301-20170228\PRSA_Data_Aotizhongxin_20130301-20170228.csv"
data_file = "..\PRSA2017_Data_20130301-20170228\PRSA_Data_20130301-20170228\simpleDataSet.csv"

def display_data():
    pd_data = pd.read_csv(data_file)
    print(f'pd_data.head(10) = \n{pd_data.head(10)}')
    mpl.rcParams['axes.unicode_minus'] = False
    sns.pairplot(pd_data, 
                x_vars = ["PM10", "SO2","NO2","CO","PRES","DEWP"],  
                y_vars = ["PM2.5"], 
                # dropna = True,
                kind = "reg", 
                height = 5,
                aspect = 0.7)
    plt.show()
