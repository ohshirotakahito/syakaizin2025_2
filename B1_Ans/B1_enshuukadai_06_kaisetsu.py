# -*- coding: utf-8 -*-
"""
演習：配送依頼を締切の早い順に並べる（解説付き解答版）

【想定する場面】
配送センターには複数の配送依頼が届いている。それぞれに優先度
（数字が小さいほど優先）と締切時刻が設定されている。
優先度を最優先にしつつ、同じ優先度の中では締切が早いものから
処理できるよう、依頼一覧を並べ替えたい。

（課題）
1. 依頼ID、締切時刻、優先度を持つ表（DataFrame）を作る。
2. 優先度→締切時刻の順で、依頼を並べ替えて表示する。
"""

import pandas as pd

requests = pd.DataFrame({
    "order_id": ["O103", "O101", "O104", "O102"],
    "deadline_hour": [17, 12, 15, 13],
    "priority": [2, 1, 1, 2],
})

# sort_values() は表を並べ替えるための関数です。
# 列名を1つだけ渡すと、その列の値の小さい順（昇順）に並びます。
#
# ["priority", "deadline_hour"] のようにリストで複数の列名を渡すと、
# 「まず1つ目の列（priority）で並べ、priorityが同じ値の行どうしは
# 2つ目の列（deadline_hour）で並べる」という、2段階の並べ替えになります。
sorted_requests = requests.sort_values(["priority", "deadline_hour"])

print(sorted_requests)

# 【ポイント】
# ・sort_values()にリストで複数の列名を渡すと、優先順位付きの並べ替えができます。
# ・降順（大きい順）にしたい列がある場合は、ascending=[True, False]のように
#   列ごとに指定することもできます。
