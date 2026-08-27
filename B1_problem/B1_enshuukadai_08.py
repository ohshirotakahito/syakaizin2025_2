# -*- coding: utf-8 -*-
"""
演習：欠測した温度センサー値を補完する

【想定する場面】
温度センサーの記録の一部が、通信不良などの理由で欠測（記録なし）に
なってしまった。欠測値をそのままにしておくと、その後の平均計算や
グラフ作成でエラーになったり、結果が不正確になったりすることがある。
そこで、欠測値を「もっともらしい値」で埋める（補完する）処理を行う。

（課題）
1. 温度の記録（一部欠測あり）を持つ表（DataFrame）を作る。
2. 欠測している値の数を確認する。
3. 欠測値を、記録全体の中央値で埋める。
"""

import numpy as np
import pandas as pd

sensor = pd.DataFrame({"temperature_c": [4.1, 4.3, np.nan, 4.0, 4.4]})

# TODO: 欠測値（NaN）の個数を表示してください
# ヒント： sensor.isna().sum().iloc[0]
print("欠損数:", None)

# TODO: temperature_c列の中央値をmedian_temperatureとして求めてください
# ヒント： sensor["temperature_c"].median()
median_temperature = None

# TODO: temperature_c列の欠測値をmedian_temperatureで埋めてください
# ヒント： sensor["temperature_c"].fillna(median_temperature)
sensor["temperature_c"] = None

print(sensor)
