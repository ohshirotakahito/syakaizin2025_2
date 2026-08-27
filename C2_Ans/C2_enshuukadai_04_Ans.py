# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#４．非線形回帰:
#
#以下のデータセットが与えられたとき、非線形回帰を利用して、xとyの間の関係をモデル化し、回帰方程式を求めてください。
#x = [1, 2, 3, 4, 5, 6]
#y = [2.5, 3.6, 7.8, 12.5, 19.7, 31.4]


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# データセット
x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([2.5, 3.6, 7.8, 12.5, 19.7, 31.4])

# 非線形関数の定義 (ここでは指数関数を使用)
def func(x, a, b, c):
    return a * np.exp(b * x) + c

# curve_fit関数を使用して非線形回帰を実行
popt, _ = curve_fit(func, x, y)

# 最適化されたパラメータを取得
a, b, c = popt

# 回帰方程式を表示
print(f'y = {a:.2f} * exp({b:.2f} * x) + {c:.2f}')

# データとフィット結果をプロット
x_line = np.arange(min(x), max(x), 0.1)
y_line = func(x_line, a, b, c)
plt.scatter(x, y, color='red', label='Data')
plt.plot(x_line, y_line, color='blue', label='Fit')
plt.legend()
plt.show()



