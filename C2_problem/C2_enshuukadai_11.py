# -*- coding: utf-8 -*-
"""
演習：複数のデータセットを結合する

（課題）
以下の2つのデータセットを結合し、全てのデータを含む新しいデータフレーム
を作成してください。
data1 = {'A': [1, 2, 3], 'B': [4, 5, 6]}
data2 = {'C': [7, 8, 9], 'D': [10, 11, 12]}

※ このファイルはTODOを埋める前でも最後まで実行できます（空の表が表示されます）。
"""

import pandas as pd

data1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
data2 = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})

# TODO: data1とdata2を横方向（列方向）に結合してください
# ヒント： pd.concat([data1, data2], axis=1)
combined_data = pd.DataFrame()  # 仮実装（空の表）

print(combined_data)
