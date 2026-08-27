# -*- coding: utf-8 -*-
"""
演習：カイ二乗検定で性別と喫煙の関連を調べる

（課題）
以下のカテゴリデータが与えられたとき、カイ二乗検定を利用して、
genderとsmokerの間に統計的に有意な関連があるかどうかを判断してください。

※ 注意：このデータは合計6件と非常に少ないため、実際にはカイ二乗検定の
前提を満たしにくい例です。検定の手順を学ぶための演習として扱ってください。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

data = {
    'gender': ['male', 'female', 'female', 'male', 'female', 'male'],
    'smoker': ['yes', 'no', 'yes', 'yes', 'no', 'no']
}
df = pd.DataFrame(data)

# TODO: genderとsmokerのクロス集計表crosstabを作ってください
# ヒント： pd.crosstab(df['gender'], df['smoker'])
crosstab = pd.DataFrame(
    np.zeros((2, 2), dtype=int),
    index=['female', 'male'],
    columns=['no', 'yes'],
)

print("【クロス集計表】")
print(crosstab)

# TODO: crosstabからカイ二乗統計量・p値・自由度・期待度数を求めてください
# ヒント： chi2_contingency(crosstab)
chi2_stat, p_value, dof, expected = 0.0, 1.0, 0, np.zeros((2, 2))

print(f"\nカイ二乗統計量: {chi2_stat:.3f}")
print(f"p値: {p_value:.5f}")
print(f"自由度: {dof}")
print("期待度数の表:")
print(expected)

if p_value < 0.05:
    print("結論：genderとsmokerの間に統計的に有意な関連があります。")
else:
    print("結論：genderとsmokerの間に統計的に有意な関連は確認できません。")
