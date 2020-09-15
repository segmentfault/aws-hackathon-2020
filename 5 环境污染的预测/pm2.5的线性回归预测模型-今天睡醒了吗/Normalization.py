import pandas as pd
import matplotlib as mpl
import seaborn as sns
import csv

from sklearn import preprocessing
from matplotlib import pyplot as plt

def Normalization():
    data_file = "..\PRSA2017_Data_20130301-20170228\PRSA_Data_20130301-20170228\simpleDataSet.csv"
    pd_data = pd.read_csv(data_file)
    sam = []
    a = ["PM10", "SO2","NO2","CO","PRES","DEWP"]
    for i in a:
        y = pd_data.loc[:, i]
        ys = list(preprocessing.scale(y))
        sam.append(ys)

    print(len(sam))
    with open('eth2.csv', 'w') as file:
        writer = csv.writer(file)
        for i in range(len(sam[0])):
            writer.writerow([sam[0][i],sam[1][i],sam[2][i],sam[3][i],sam[4][i],sam[5][i]])
