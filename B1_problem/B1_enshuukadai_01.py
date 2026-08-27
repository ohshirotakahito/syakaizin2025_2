# -*- coding: utf-8 -*-
"""
演習：10店舗の販売数をNumPy配列で扱う

【想定する場面】
10店舗を展開するチェーン店で、各店舗の本日の販売数が集計された。
店舗番号と販売数を対応させて管理し、全店合計と平均を求めたい。

（課題）
1. 店舗番号（1～10）をNumPy配列として作る。
2. 各店舗の販売数をNumPy配列として作る。
3. 全店の合計販売数と、平均販売数を求めて表示する。
"""

import numpy as np

# TODO: 1以上11未満の連続整数（1～10）を持つ配列store_numbersを作ってください
# ヒント： np.arange(1, 11)
store_numbers = None

# TODO: 10店舗ぶんの販売数を持つ配列daily_salesを作ってください
# ヒント： np.array([82, 95, 71, 104, 88, 120, 67, 99, 110, 91])
daily_sales = None

print("店舗番号:", store_numbers)
print("販売数:", daily_sales)

# TODO: daily_salesの合計と平均を使って、下のメッセージを完成させてください
# ヒント： daily_sales.sum()、daily_sales.mean()
print(f"全店合計={None}個、平均={None}個")
