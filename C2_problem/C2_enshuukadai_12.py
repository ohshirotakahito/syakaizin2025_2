# -*- coding: utf-8 -*-
"""
演習：データのグルーピングと集計を行う

（課題）
以下のデータセットに対して、'Gender'列でデータをグルーピングし、
各グループの'Age'の平均値を計算してください。
data = {'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 'Age': [23, 45, 34, 30, 25]}

※ このファイルはTODOを埋める前でも最後まで実行できます（空の表が表示されます）。
"""

import pandas as pd

data = pd.DataFrame({'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 'Age': [23, 45, 34, 30, 25]})

# TODO: Gender列でグループ化し、各グループのAgeの平均を求めてください
# ヒント： data.groupby('Gender').mean(numeric_only=True)
grouped_data = pd.DataFrame()  # 仮実装（空の表）

print(grouped_data)
