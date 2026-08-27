# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#１１．複数のデータセットの結合:
#
#以下の2つのデータセットを結合し、全てのデータを含む新しいデータフレームを作成してください。
#data1 = {'A': [1, 2, 3], 'B': [4, 5, 6]}
#data2 = {'C': [7, 8, 9], 'D': [10, 11, 12]}

import pandas as pd

# データセットの定義
data1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
data2 = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})

# 複数のデータセットの結合
combined_data = pd.concat([data1, data2], axis=1)

# 結合したデータを表示
print(combined_data)




