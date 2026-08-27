# -*- coding: utf-8 -*-
"""
演習：非線形回帰でxとyの関係をモデル化する

（課題）
以下のデータセットが与えられたとき、非線形回帰を利用して、xとyの間の
関係をモデル化し、回帰方程式を求めてください。
x = [1, 2, 3, 4, 5, 6]
y = [2.5, 3.6, 7.8, 12.5, 19.7, 31.4]

※ このファイルはTODOを埋める前でも最後まで実行できます。
   func()は仮に「直線（1次式）」になっているため、フィットはうまくいきません。
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([2.5, 3.6, 7.8, 12.5, 19.7, 31.4])


def func(x, a, b, c):
    """当てはめたい非線形モデル。"""
    # TODO: 指数関数 a * exp(b * x) + c の式に書き換えてください
    # ヒント： return a * np.exp(b * x) + c
    return a * x + c  # 仮実装（直線）


popt, _ = curve_fit(func, x, y)
a, b, c = popt

print(f'回帰方程式: y = {a:.2f} * exp({b:.2f} * x) + {c:.2f}')

x_line = np.arange(min(x), max(x), 0.1)
y_line = func(x_line, a, b, c)
plt.scatter(x, y, color='red', label='Data')
plt.plot(x_line, y_line, color='blue', label='Fit')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(alpha=0.25)
plt.show()
