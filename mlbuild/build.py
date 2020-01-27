"""Обучение модели Catboostclassifier, результат - файл catboost.obj"""

__author__ = 'alexander'
__maintainer__ = 'alexander'
__credits__ = ['alexander', ]
__copyright__ = "LGPL"
__status__ = 'Development'
__version__ = '20200127'

import os
from skimage.io import imread
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import time
from catboost import CatBoostClassifier
import _pickle as cPickle

N = 200
M = 1000
T = 4


def _spam_extract(im, color):
    """Извлечение spam-feature"""
    mask = np.zeros((N, N, 3))
    for i in range(N):
        for j in range(N-1):
            mask[i][j] += im[i][j] 
            mask[i][j] -= im[i][j+1]
    dim = T*2+1
    spam_feature = np.zeros((dim,dim))
    count_cond = np.zeros((dim,dim))
    for u in range(-T,T+1):
        for v in range(-T,T+1):
          for i in range(N):
            for j in range(N-1):
              if mask[i][j][color] == u:
                count_cond[u+T,v+T] += 1
                if mask[i][j+1][color] == v:
                  spam_feature[u+T,v+T] += 1
    spam_feature /= count_cond
    spam_feature = spam_feature.reshape((1, dim*dim))[0]
    return spam_feature


print('0 done')
print(time.ctime())
df = pd.DataFrame(columns=range(2+3*9*9))
s=0
path = '/train/steg/'
for fn in os.listdir(path):
    im = imread(path+fn) 
    x = np.array([fn, 1])  
    x = np.concatenate((x, _spam_extract(im, 0)))
    x = np.concatenate((x, _spam_extract(im, 1)))
    x = np.concatenate((x, _spam_extract(im, 2)))
    df.loc[s] = x
    s+=1
    if (s % 100 == 0):
        print('{} done'.format(s))
        print(time.ctime())
path = '/train/clean/'
for fn in os.listdir(path):
    im = imread(path+fn)
    x = np.array([fn, 0])
    x = np.concatenate((x, _spam_extract(im, 0)))
    x = np.concatenate((x, _spam_extract(im, 1)))
    x = np.concatenate((x, _spam_extract(im, 2)))
    df.loc[s] = x
    s+=1
    if (s % 100 == 0):
        print('{} done'.format(s))
        print(time.ctime())
df.to_csv('features.csv')

df = pd.read_csv('features.csv')
df = df.drop(columns=['Unnamed: 0'])
df = shuffle(df)
df = df.reset_index(drop = True)
df.replace('nan', np.nan, inplace=True)
df.fillna(0, inplace=True)

X = df.iloc[:M, 2:]
y = df['1'][:M].values
X.transpose()
P = df.iloc[:, 2:]
P = P.transpose()

cat_tree = CatBoostClassifier(iterations=50)
cat_tree.fit(X, y)

with open('catboost.obj', 'wb') as f:
    cPickle.dump(cat_tree, f)