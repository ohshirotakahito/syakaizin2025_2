# -*- coding: utf-8 -*-
"""
演習：k-meansクラスタリングでセントロイドを求める

（課題）
以下のデータセットが与えられたとき、k-meansクラスタリングを利用して、
データをクラスタリングし、それぞれのクラスターのセントロイド（重心）を
決定してください。
data = [[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]]

※ このファイルはTODOを埋める前でも最後まで実行できます
   （仮実装ではdataの代わりにゼロ配列で学習するため、結果は正しくありません）。
"""

from sklearn.cluster import KMeans
import numpy as np

data = np.array([[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]])

# TODO: KMeans(n_clusters=2, random_state=0)をdataでfit()してください
# ヒント： KMeans(n_clusters=2, random_state=0).fit(data)
kmeans = KMeans(n_clusters=2, random_state=0).fit(np.zeros_like(data))  # 仮実装

print('Cluster centroids:\n', kmeans.cluster_centers_)
print('Cluster labels:\n', kmeans.labels_)
