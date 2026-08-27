# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#３．カイ二乗検定:
#
#以下のカテゴリデータが与えられたとき、カイ二乗検定を利用して、genderとsmokerの間に統計的に有意な関連があるかどうかを判断してください。
#data = {
#    'gender': ['male', 'female', 'female', 'male', 'female', 'male'],
#    'smoker': ['yes', 'no', 'yes', 'yes', 'no', 'no']
#}


import pandas as pd
from scipy.stats import chi2_contingency

# データをPandasデータフレームに変換
data = {
    'gender': ['male', 'female', 'female', 'male', 'female', 'male'],
    'smoker': ['yes', 'no', 'yes', 'yes', 'no', 'no']
}
df = pd.DataFrame(data)

# クロスタブを作成
crosstab = pd.crosstab(df['gender'], df['smoker'])

# カイ二乗検定を実行
chi2_stat, p_value, dof, ex = chi2_contingency(crosstab)

# 結果を表示
print(f'Chi2 Stat: {chi2_stat}')
print(f'P Value: {p_value}')
print(f'Degrees of Freedom: {dof}')
print('Expected Frequency Table:')
print(ex)

# p値が0.05未満の場合、genderとsmokerの間に統計的に有意な関連があると結論付ける
if p_value < 0.05:
    print('There is a statistically significant relationship between gender and smoker.')
else:
    print('There is no statistically significant relationship between gender and smoker.')



