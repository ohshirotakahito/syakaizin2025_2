# -*- coding: utf-8 -*-
"""
演習：zスコアを用いて異常値を検出する

（課題）
以下のデータセットに対して、zスコアを用いて異常値を検出してください。

※ このファイルはTODOを埋める前でも最後まで実行できます（異常値なしと表示されます）。
"""

import numpy as np
from scipy.stats import zscore

data = [34, 36, 36, 38, 38, 39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 1000]
data = np.array(data)

# TODO: dataのzスコアz_scoresを求めてください
# ヒント： zscore(data)
z_scores = np.zeros_like(data, dtype=float)

# TODO: |zスコア|が3を超える位置をoutliersとして求めてください
# ヒント： np.where(np.abs(z_scores) > 3)
outliers = np.where(np.abs(z_scores) > 3)

print('異常値と判定された値: ', data[outliers])
