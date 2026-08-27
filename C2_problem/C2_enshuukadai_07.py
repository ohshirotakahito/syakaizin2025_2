# -*- coding: utf-8 -*-
"""
演習：階層的クラスタリングでデンドログラムを作成する

（課題）
以下のデータセットが与えられたとき、階層的クラスタリングを利用して、
デンドログラムを作成し、クラスターの数を決定してください。
data = [[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]]

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

data = [[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]]

# TODO: 'ward'法で階層的クラスタリングを実行し、結合の履歴Zを求めてください
# ヒント： linkage(data, 'ward')
Z = linkage(data, 'ward')

plt.figure(figsize=(10, 7))
dendrogram(Z)
plt.title('Dendrogram')
plt.xlabel('Data Points')
plt.ylabel('Euclidean Distances')
plt.show()

# TODO: デンドログラムを見て、適切と思うクラスター数をnum_clustersに入れてください
num_clusters = None
print(f"デンドログラムから決定したクラスター数: {num_clusters}")
