# -*- coding: utf-8 -*-
"""
演習：東西2拠点の研修名簿を縦に結合する

【想定する場面】
東日本拠点と西日本拠点で、それぞれ別々に研修の参加者名簿を作っていた。
全社的な集計をするために、2つの表を1つの表にまとめたい。
どちらの拠点の参加者かが分かるよう、拠点名の列も追加しておく。

（課題）
1. 東日本拠点の参加者名簿（DataFrame）を作り、拠点名の列を追加する。
2. 西日本拠点の参加者名簿（DataFrame）を作り、拠点名の列を追加する。
3. 2つの表を縦に結合し、1つの表として表示する。
"""

import pandas as pd

east = pd.DataFrame({"employee": ["Sato", "Ito"], "score": [82, 91]})
east["office"] = "East"

west = pd.DataFrame({"employee": ["Tanaka", "Mori"], "score": [78, 88]})
west["office"] = "West"

# TODO: eastとwestを縦に結合し、行番号を振り直したall_participantsを作ってください
# ヒント： pd.concat([east, west], ignore_index=True)
all_participants = None

print(all_participants)
