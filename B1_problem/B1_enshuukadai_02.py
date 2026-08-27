# -*- coding: utf-8 -*-
"""
演習：研修参加者名簿をDataFrameで作る

【想定する場面】
社内研修の参加者について、氏名・所属部署・研修の得点を1つの表として
まとめて管理したい。

（課題）
1. 参加者の氏名、所属部署、得点をまとめたDataFrame（表形式のデータ）を作る。
2. 作成した表と、表が持つ列名の一覧を表示する。
"""

import pandas as pd

# TODO: employee（氏名）、department（所属）、score（得点）の3列を持つ
#       DataFrame participants を作ってください
# ヒント： pd.DataFrame({
#             "employee": ["Sato", "Suzuki", "Takahashi"],
#             "department": ["Sales", "IT", "Production"],
#             "score": [82, 91, 76],
#         })
participants = None

print(participants)

# TODO: participantsの列名の一覧をリストとして表示してください
# ヒント： participants.columns.tolist()
print("\n列名:", None)
