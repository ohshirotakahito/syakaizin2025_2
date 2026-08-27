# -*- coding: utf-8 -*-
"""
演習：発注点以下の在庫商品を抽出する（解説付き解答版）

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

# inventory["stock"] <= inventory["reorder_point"] は、
# 「在庫数」列と「発注点」列を1行ずつ比較し、条件を満たすかどうかを
# True/Falseで表した列（正確にはSeriesと呼ばれるpandasの1列データ）を作ります。
#
# inventory[条件] のように、DataFrameへ角括弧でTrue/Falseの列を渡すと、
# Trueだった行だけを取り出す「絞り込み（フィルタリング）」ができます。
reorder = inventory[inventory["stock"] <= inventory["reorder_point"]]

print("【要発注商品】")
print(reorder)

# 【ポイント】
# ・「表 [ 条件式 ]」という書き方は、pandasで最もよく使う絞り込みの基本形です。
# ・条件式の部分だけを別の変数に入れてから使うと、コードが読みやすくなることもあります。
#   例： is_low_stock = inventory["stock"] <= inventory["reorder_point"]
#       reorder = inventory[is_low_stock]
