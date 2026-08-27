# -*- coding: utf-8 -*-
"""
演習：東西2拠点の研修名簿を縦に結合する（解説付き解答版）

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
# 表全体へ同じ値を代入すると、その値がすべての行に入った新しい列ができます。
# ここでは、東日本拠点であることが分かるよう"office"列に"East"を入れています。
east["office"] = "East"

west = pd.DataFrame({"employee": ["Tanaka", "Mori"], "score": [78, 88]})
west["office"] = "West"

# pd.concat([表1, 表2]) は、複数の表を縦に（行方向に）結合します。
# 2つの表の列名が同じ（employee, score, office）なので、そのままつながります。
#
# ignore_index=True を付けないと、結合後もそれぞれの表がもともと持っていた
# 行番号（0, 1, 0, 1, ...）がそのまま残ってしまい、番号が重複します。
# ignore_index=True にすると、結合後の行番号を0から振り直してくれます。
all_participants = pd.concat([east, west], ignore_index=True)

print(all_participants)

# 【ポイント】
# ・列名が同じ表同士は、pd.concat()で縦に簡単につなげられます。
# ・結合後は行番号が重複しやすいので、ignore_index=Trueを付ける習慣をつけましょう。
