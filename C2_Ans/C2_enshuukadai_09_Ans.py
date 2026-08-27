# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#９．欠損値の補完:
#
#以下のデータセットに対して、欠損値を平均値で補完してください。
#ldata = {'A': [12, np.nan, 34, 56], 'B': [45, 67, np.nan, 78]}



import pandas as pd
import numpy as np

# データセット
data = pd.DataFrame({'A': [12, np.nan, 34, 56], 'B': [45, 67, np.nan, 78]})

# 補完前のデータを表示
print(data)

# 欠損値を列の平均値で補完
imputed_data = data.fillna(data.mean())

# 補完後のデータを表示
print(imputed_data)



