# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#６．主成分分析（PCA）:
#
#以下のデータセットが与えられたとき、主成分分析（PCA）を利用して、データの次元を削減し、第一主成分と第二主成分をプロットしてください。
#data = [[2.5, 3.4, 2.7], [3.6, 4.5, 3.8], [2.9, 3.9, 2.6], [4.2, 5.1, 4.3], [3.1, 3.7, 3.2]]


import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# データセット
data = [[2.5, 3.4, 2.7], [3.6, 4.5, 3.8], [2.9, 3.9, 2.6], [4.2, 5.1, 4.3], [3.1, 3.7, 3.2]]

# PCAのインスタンスを作成し、データをフィット
pca = PCA(n_components=2)  # 2つの主成分を保持するように指定
pca_result = pca.fit_transform(data)

# 第一主成分と第二主成分をプロット
plt.scatter(pca_result[:, 0], pca_result[:, 1])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA Result')
plt.grid(True)
plt.show()




