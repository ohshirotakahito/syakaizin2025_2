# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#２．ANOVA（分散分析）:
#
#以下の3つのサンプルデータセットが与えられたとき、ANOVAを利用して、これら3つのグループの平均値が統計的に異なるかどうかを判断してください。
#group1 = [12.23, 15.45, 14.67, 18.56, 14.29]
#group2 = [23.45, 25.67, 22.34, 21.56, 25.89]
#group3 = [32.13, 34.89, 31.78, 33.56, 32.45]

from scipy import stats

# サンプルデータセット
group1 = [12.23, 15.45, 14.67, 18.56, 14.29]
group2 = [23.45, 25.67, 22.34, 21.56, 25.89]
group3 = [32.13, 34.89, 31.78, 33.56, 32.45]

# ANOVAを実行
f_stat, p_value = stats.f_oneway(group1, group2, group3)

# 結果を表示
print(f'F-statistic: {f_stat}')
print(f'P-value: {p_value}')

# p値が0.05未満の場合、グループの平均値は統計的に異なると結論付ける
if p_value < 0.05:
    print('The means of the groups are statistically significantly different.')
else:
    print('The means of the groups are not statistically significantly different.')


