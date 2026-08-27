# -*- coding: utf-8 -*-
"""
演習：主成分分析（PCA）でデータの次元を削減する

（課題）
以下のデータセットが与えられたとき、主成分分析（PCA）を利用して、
データの次元を削減し、第一主成分と第二主成分をプロットしてください。
data = [[2.5, 3.4, 2.7], [3.6, 4.5, 3.8], [2.9, 3.9, 2.6], [4.2, 5.1, 4.3], [3.1, 3.7, 3.2]]

※ このファイルはTODOを埋める前でも最後まで実行できます（点はすべて原点になります）。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

data = [[2.5, 3.4, 2.7], [3.6, 4.5, 3.8], [2.9, 3.9, 2.6], [4.2, 5.1, 4.3], [3.1, 3.7, 3.2]]

pca = PCA(n_components=2)

# TODO: dataをPCAで学習・変換し、pca_resultを求めてください
# ヒント： pca.fit_transform(data)
pca_result = np.zeros((len(data), 2))

plt.scatter(pca_result[:, 0], pca_result[:, 1])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA Result')
plt.grid(True)
plt.show()
