# -*- coding: utf-8 -*-
"""
演習：研修参加者名簿をDataFrameで作る（解説付き解答版）

【想定する場面】
社内研修の参加者について、氏名・所属部署・研修の得点を1つの表として
まとめて管理したい。

（課題）
1. 参加者の氏名、所属部署、得点をまとめたDataFrame（表形式のデータ）を作る。
2. 作成した表と、表が持つ列名の一覧を表示する。
"""

import pandas as pd

# pandasは、Excelの表のような「行と列を持つデータ」をPythonで扱うための
# 代表的なライブラリです。表全体を表す型を DataFrame（データフレーム）と呼びます。

# pd.DataFrame()へ辞書（dict）を渡すと、表を作ることができます。
# 辞書の「キー」がそのまま列名になり、「値のリスト」がその列の中身になります。
# ここでは employee（氏名）、department（所属）、score（得点）という3つの列を持つ
# 3人分（3行）の表を作っています。
participants = pd.DataFrame({
    "employee": ["Sato", "Suzuki", "Takahashi"],
    "department": ["Sales", "IT", "Production"],
    "score": [82, 91, 76],
})

print(participants)

# .columns は表が持つ列名の一覧を返します。
# .tolist() を付けると、Pythonの普通のリスト（例：['employee', 'department', 'score']）
# の形にできるので、printしたときに見やすくなります。
print("\n列名:", participants.columns.tolist())

# 【ポイント】
# ・DataFrameは「列名付きの表」というイメージで、Excelの1つのシートに近いものです。
# ・辞書のキーが列名、リストの各要素がその列の各行の値に対応します。
