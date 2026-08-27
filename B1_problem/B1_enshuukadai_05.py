# -*- coding: utf-8 -*-
"""
演習：発注点以下の在庫商品を抽出する

【想定する場面】
在庫管理では、商品ごとに「発注点」（このレベルを下回ったら追加発注する
目安の数量）が決められている。在庫数が発注点以下になっている商品を
自動的に見つけ出したい。

（課題）
1. 商品名、在庫数、発注点を持つ表（DataFrame）を作る。
2. 在庫数が発注点以下の商品だけを抽出して表示する。
"""

import pandas as pd

inventory = pd.DataFrame({
    "product": ["Coffee beans", "Milk", "Cups", "Tea"],
    "stock": [18, 7, 240, 12],
    "reorder_point": [20, 10, 100, 15],
})

# TODO: 在庫数(stock)が発注点(reorder_point)以下の行だけを
#       抽出したreorderを作ってください
# ヒント： inventory[inventory["stock"] <= inventory["reorder_point"]]
reorder = None

print("【要発注商品】")
print(reorder)
