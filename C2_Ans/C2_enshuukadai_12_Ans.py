# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#１２．データのグルーピングと集計:
#以下のデータセットに対して、'Gender'列でデータをグルーピングし、各グループの'Age'の平均値を計算してください。
#data = {'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 'Age': [23, 45, 34, 30, 25]}


import pandas as pd

# データセットの定義
data = pd.DataFrame({'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 'Age': [23, 45, 34, 30, 25]})

# 'Gender'列でデータをグルーピングし、各グループの'Age'の平均値を計算
grouped_data = data.groupby('Gender').mean()

# 結果を表示
print(grouped_data)




