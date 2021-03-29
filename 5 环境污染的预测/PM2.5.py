import pandas as pd
from pandas import DataFrame

# train_df = pd.read_csv("/Users/m-mac/Desktop/pm256497/GW_MajPM25pollY.csv")
# #显示所有列
# pd.set_option('display.max_columns', None)
# print("--------------raw_data------------------")
# print(train_df)
# print("----------------------------------------")
# print("--------------data_info------------------")
# print(train_df.info())
# print("----------------------------------------")
# print("--------------data_des------------------")
# print(train_df.describe())
# print("----------------------------------------")
from sklearn.linear_model import LogisticRegressionCV, LinearRegression
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split


def preProcess_data(path):
    train_df = pd.read_csv(path)
    future_array = train_df.iloc[1:200000, 0].values
    list_future = []
    for item in future_array:
        list_future.append(str(item).split('\t'))
    train_df = DataFrame(list_future)
    train_df = train_df[(train_df[7] == '人口暴露于PM2.5年均浓度') & (~train_df[8].str.contains('E'))]
    return train_df


# train_df1 = preProcess_data('./pm256497/GW_MajPM25pollY.csv');
# train_df4 = preProcess_data('./pm256497/GW_PM25pollY.csv');
# pd.np.set_printoptions(suppress=True)
print("data loading...")
train_df2 = preProcess_data('./pm256497/GW_PM25pollRegY.csv');
train_df3 = preProcess_data('./pm256497/GW_PM25pollRegY1.csv');
train_df = pd.concat([train_df2, train_df3], ignore_index=True)
# label_list = [for str in train_df[8].values]
label_list = []
for item in train_df[8].values:
    if 'E' in item:
        label_list.append(12)
    else:
        label_list.append(float(item))

# for item in train_df[8].values:
#     if len(item.split(" ")) != 2:
#         label_list.append(float(item))
#         continue
#     label_list.append(float(item.split(" ")[1]))
train_df = train_df.drop([2, 3, 7, 8, 9], axis=1)
train_list = pd.get_dummies(train_df).values

# cv = 5
print("data train...")
clf = LinearRegression()
train, valid, train_label, valid_label = train_test_split(train_list, label_list, test_size=0.5, random_state=2020)
clf.fit(train, train_label)
# pred1 = clf.predict(train)
# accuracy1 = clf.score(valid, valid_label)
# print(accuracy1)
# print('在训练集上的精确度:%.4f'%accuracy1)

print("data predict...")
print(clf.score(train, train_label))  # 精度
# print('训练集准确率：', accuracy_score(train_label, clf.predict(train)))
print(clf.score(valid, valid_label))
# print('测试集准确率：', accuracy_score(valid_label, clf.predict(valid)))

# auc = roc_auc_score(valid_label, clf.predict_proba(valid)[:, 1])
# auc = roc_auc_score(valid_label, clf.predict_proba(valid)[:, 1])
# print("Validation SET ROC-AUC Score {} ".format(auc))

print("finish")

# 显示所有列
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', 1000)
# pd.set_option("display.max_colwidth",1000)
# pd.set_option('display.width',1000)
# print("--------------raw_data------------------")
# print(train_df)
# print("----------------------------------------")
# print("--------------data_info------------------")
# print(train_df.info())
# print("----------------------------------------")
# print("--------------data_des------------------")
# print(train_df.describe())
# print("----------------------------------------")
