# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#８．k-meansクラスタリング:
#
#以下のデータセットが与えられたとき、k-meansクラスタリングを利用して、データをクラスタリングし、それぞれのクラスターのセントロイド（重心）を決定してください。
#data = [[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]]


from sklearn.cluster import KMeans
import numpy as np

# データセット
data = np.array([[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]])

# k-meansクラスタリングの実行
kmeans = KMeans(n_clusters=2, random_state=0).fit(data)

# クラスターのセントロイドを表示
print('Cluster centroids:\n', kmeans.cluster_centers_)

# クラスターのラベルを表示（どのデータポイントがどのクラスターに属しているか）
print('Cluster labels:\n', kmeans.labels_)



