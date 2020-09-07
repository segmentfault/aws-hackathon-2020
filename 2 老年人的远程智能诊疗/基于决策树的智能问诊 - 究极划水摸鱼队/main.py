import pandas as pd
import numpy as np
import pickle
from translate import Translator
from utils import *
import joblib
import jieba


feature_names = get_feature_names('feature_names.pkl')
target_names = get_target_names('target_names.pkl')
clf = get_model('clf.pkl')

while True:
    symptom = input('请输入您的症状：')
    if symptom == 'q':
        print('再见')
        break
    symptom = remove_pun(symptom)
    symptom = jieba.cut(symptom, cut_all=False)
    symptom = [s for s in symptom]
    x = get_x(symptom, feature_names).reshape(1, -1)
    translator = Translator(to_lang="chinese")
    disease = translator.translate(target_names[clf.predict(x)[0]])
    print('您的疾病有可能是：{}'.format(disease))