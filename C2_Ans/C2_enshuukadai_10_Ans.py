# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#１０．異常値の検出:
#
#以下のデータセットに対して、zスコアを用いて異常値を検出してください。
#data = [34, 36, 36, 38, 38, 39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 1000]

import numpy as np
from scipy.stats import zscore

data = [34, 36, 36, 38, 38, 39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 1000]

# データを定義
data = np.array(data)

# zスコアを計算
z_scores = zscore(data)
outliers = np.where(np.abs(z_scores) > 3)

# 異常値の表示:
print('Outlier values: ', np.array(data)[outliers])



