import numpy as np
import pickle
import joblib


def is_ch(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False


def remove_pun(txt):
    new_txt = ''
    for char in txt:
        if is_ch(char):
            new_txt += char
    return new_txt


def str2vec(str1, str2):
    str1_set = set(str1)
    str2_set = set(str2)
    union = str1_set | str2_set
    vec1 = []
    vec2 = []
    for char in union:
        if char in str1_set:
            vec1.append(1)
        else:
            vec1.append(0)
        if char in str2_set:
            vec2.append(1)
        else:
            vec2.append(0)
    return np.array(vec1), np.array(vec2)


def cosine_similarity(x, y):
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    return num / denom


def get_feature_names(path):
    with open(path, 'rb') as f:
        feature_names = pickle.load(f)
    return feature_names


def get_target_names(path):
    with open(path, 'rb') as f:
        target_names = pickle.load(f)
    return target_names


def get_x(symptom, feature_names):
    x = [0] * len(feature_names)
    for s in symptom:
        sim = np.array(list(map(lambda x: cosine_similarity(*str2vec(s, x)), feature_names)))
        if sim.max() > 0:
            x[sim.argmax()] = 1
    return np.array(x)


def get_model(path):
    return joblib.load(path)