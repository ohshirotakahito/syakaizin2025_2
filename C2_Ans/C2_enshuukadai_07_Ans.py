# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#７．階層的クラスタリング:
#
#以下のデータセットが与えられたとき、階層的クラスタリングを利用して、デンドログラムを作成し、クラスターの数を決定してください。
#data = [[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]]

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# データセット
data = [[2.5, 3.4], [3.6, 4.5], [2.9, 3.9], [4.2, 5.1], [3.1, 3.7]]

# 階層的クラスタリングの実行
Z = linkage(data, 'ward')

# デンドログラムの作成
plt.figure(figsize=(10, 7))
dendrogram(Z)
plt.title('Dendrogram')
plt.xlabel('Data Points')
plt.ylabel('Euclidean Distances')
plt.show()

# デンドログラムを解釈してクラスター数を決定する（例えば、クラスター数を3とする）
num_clusters = 3




