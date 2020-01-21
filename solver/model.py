"""Обработчик изображения и прогон через обученный catboost"""

__author__ = 'alexander'
__maintainer__ = 'alexander'
__credits__ = ['alexander', ]
__copyright__ = "LGPL"
__status__ = 'Development'
__version__ = '20200121'


import _pickle as cPickle
import pandas as pd
import numpy as np
from skimage.io import imread
import io
from catboost import CatBoostClassifier
T = 4
N = 200


def _spam_extract(im, color):
    """Извлечение spam-feature"""
    n = min(N, im.shape[0], im.shape[1])
    mask = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n-1):
            mask[i][j] += im[i][j]
            mask[i][j] -= im[i][j+1]
    dim = T*2+1
    spam_feature = np.zeros((dim, dim))
    count_cond = np.zeros((dim, dim))
    for u in range(-T, T+1):
        for v in range(-T, T+1):
            for i in range(n):
                for j in range(n-1):
                    if mask[i][j][color] == u:
                        count_cond[u+T, v+T] += 1
                        if mask[i][j+1][color] == v:
                            spam_feature[u+T, v+T] += 1
    spam_feature /= count_cond
    spam_feature = spam_feature.reshape((1, dim*dim))[0]
    return spam_feature


def steg_search(data, fn) -> list:
    """
    Стегоанализ изображения
    :param data: переданное изображение
    :param fn: id файла для дальнейшей записи в БД
    :return: массив 2 значений - id файла и результат поиска стеганографии
    """
    df = pd.DataFrame(columns=range(1+3*(2*T+1)*(2*T+1)))
    im = imread(io.BytesIO(data))
    if im.shape[2] == 4:
        im2 = np.zeros((im.shape[0], im.shape[1], 3))
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                im2[i][j] = im[i][j][:3]
        im = im2
    x = np.array([fn])
    x = np.concatenate((x, _spam_extract(im, 0)))
    x = np.concatenate((x, _spam_extract(im, 1)))
    x = np.concatenate((x, _spam_extract(im, 2)))
    df.loc[0] = x
    with open('solver/catboost.obj', 'rb') as f:
        cat_tree = cPickle.load(f)
    p = df.iloc[:, 1:]
    p = p.transpose()
    res = []
    for i in range(len(df[0])):
        res.append([df[0][i], cat_tree.predict([p[i].tolist()])[0]])
    return res
