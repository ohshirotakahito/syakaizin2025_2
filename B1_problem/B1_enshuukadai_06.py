# -*- coding: utf-8 -*-
"""
演習：配送依頼を締切の早い順に並べる

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

# TODO: priority（優先度）→deadline_hour（締切時刻）の順で並べ替えた
#       sorted_requestsを作ってください
# ヒント： requests.sort_values(["priority", "deadline_hour"])
sorted_requests = None

print(sorted_requests)
