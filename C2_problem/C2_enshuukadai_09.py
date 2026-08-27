# -*- coding: utf-8 -*-
"""
演習：欠損値を平均値で補完する

（課題）
以下のデータセットに対して、欠損値を平均値で補完してください。
data = {'A': [12, np.nan, 34, 56], 'B': [45, 67, np.nan, 78]}

※ このファイルはTODOを埋める前でも最後まで実行できます（欠損値がそのまま残ります）。
"""

import pandas as pd
import numpy as np

data = pd.DataFrame({'A': [12, np.nan, 34, 56], 'B': [45, 67, np.nan, 78]})

print("【補完前のデータ】")
print(data)

# TODO: dataの欠損値を、各列の平均値で補完してください
# ヒント： data.fillna(data.mean())
imputed_data = data.copy()  # 仮実装（まだ補完していない）

print("\n【補完後のデータ】")
print(imputed_data)
