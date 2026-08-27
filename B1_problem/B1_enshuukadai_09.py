# -*- coding: utf-8 -*-
"""
演習：売上表へ客単価を追加し、一時列を削除する

【想定する場面】
店舗ごとの売上金額と来店客数のデータから、「客単価」（お客様1人あたりの
平均購入金額）を計算したい。社内分析では来店客数の列も残しておきたいが、
外部への報告資料では客単価だけを見せたいので、報告用には来店客数の列を
取り除いた表を作る。

（課題）
1. 店舗名、売上金額、来店客数を持つ表（DataFrame）を作る。
2. 売上金額 ÷ 来店客数で「客単価」の列を追加する。
3. 外部報告用に、来店客数の列を取り除いた表を作る。
"""

import pandas as pd

sales = pd.DataFrame({
    "store": ["Tokyo", "Osaka", "Fukuoka"],
    "sales_yen": [520000, 430000, 310000],
    "customers": [410, 370, 260],
})

# TODO: 売上金額(sales_yen) ÷ 来店客数(customers)で"sales_per_customer"列を追加してください
# ヒント： sales["sales_yen"] / sales["customers"]
sales["sales_per_customer"] = None

print(sales.round(1))

# TODO: customers列を取り除いた表reportを作ってください
# ヒント： sales.drop(columns="customers")
report = None

print("\n【外部報告用】")
print(report.round(1))
