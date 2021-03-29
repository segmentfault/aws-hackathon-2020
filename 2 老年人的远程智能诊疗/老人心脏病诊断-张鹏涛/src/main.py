from sklearn.model_selection import train_test_split
import sagemaker
from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import get_image_uri
from sagemaker.predictor import csv_serializer
from utils import read_data
from sklearn.metrics import accuracy_score
import os
import pandas as pd
import sys
sys.path.append("./")

data_file = "../data/data_raw.csv"
data_columns = ["ATTR" + str(i) for i in range(1, 14)]
data_columns.append("Label")

X, Y = read_data(data_file=data_file, data_columns=data_columns)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

pd.concat([X_train, y_train], axis=1).to_csv("../data/train.csv", index=False)
pd.concat([X_test, y_test], axis=1).to_csv("../data/test.csv", index=False)

# 将原始的数据以及处理好的数据集存储到s3上面
session = sagemaker.Session()
data_dir = "../data/"
prefix = 'sentiment-web-app'

test_location = session.upload_data(os.path.join(data_dir, 'test.csv'), key_prefix=prefix)
train_location = session.upload_data(os.path.join(data_dir, 'train.csv'), key_prefix=prefix)

# 使用sagemaker来进行模型的训练
role = get_execution_role()

container = get_image_uri(session.boto_region_name, 'xgboost')

xgb = sagemaker.estimator.Estimator(container,
                                    role,
                                    train_instance_count=1,
                                    train_instance_type='ml.m4.xlarge',
                                    output_path='s3://{}/{}/output'.format(session.default_bucket(), prefix),
                                    sagemaker_session=session)

# 指定xgb需要的参数
xgb.set_hyperparameters(max_depth=5,
                        eta=0.2,
                        gamma=4,
                        min_child_weight=6,
                        subsample=0.8,
                        silent=0,
                        objective='binary:logistic',
                        early_stopping_rounds=10,
                        num_round=500)
# 从s3中读取数据
s3_input_train = sagemaker.s3_input(s3_data=train_location, content_type='csv')
s3_input_test = sagemaker.s3_input(s3_data=test_location, content_type='csv')

# 模型训练
xgb.fit({'train': s3_input_train, 'test': s3_input_test})

# 模型测试
xgb_transformer = xgb.transformer(instance_count=1, instance_type='ml.m4.xlarge')

xgb_transformer.transform(test_location, content_type='text/csv', split_type='Line')

xgb_transformer.wait()

predictions = pd.read_csv(os.path.join(data_dir, 'test.csv.out'), header=None)
predictions = [round(num) for num in predictions.squeeze().values]

accuracy_score(y_test, predictions)

# 模型的部署
xgb_predictor = xgb.deploy(initial_instance_count=1, instance_type='ml.m4.xlarge')
