# -*- coding: utf-8 -*-
"""
演習：吸光度の検量線から未知試料濃度を推定する

【想定する場面】
既知濃度の標準液から作った検量線（濃度と吸光度の関係を表す直線）を使い、
濃度が分からない未知試料の吸光度から、その濃度を逆算して推定したい。

（課題）
1. 標準液の濃度と吸光度から、線形回帰で検量線（直線の式）を求める。
2. 求めた検量線の式を、切片と傾きの形で表示する。
3. 未知試料の吸光度から、検量線の式を逆算して濃度を推定する。
4. 標準液・検量線・推定した未知試料の点をグラフに表示する。
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([0.00, 0.02, 0.04, 0.06, 0.08, 0.10]).reshape(-1, 1)
y = np.array([0.01, 0.16, 0.31, 0.47, 0.61, 0.76])

# TODO: LinearRegressionをXとyで学習させてください
# ヒント： LinearRegression().fit(X, y)
model = None

unknown_absorbance = 0.40

# TODO: 検量線の式 Abs = coef * C + intercept をCについて解いて、
#       unknown_absorbanceに対応する濃度unknown_concentrationを求めてください
# ヒント： (unknown_absorbance - model.intercept_) / model.coef_[0]
unknown_concentration = None

print(f"検量線: Abs={model.coef_[0]:.3f}*C+{model.intercept_:.3f}")
print(f"吸光度{unknown_absorbance:.2f}の推定濃度: {unknown_concentration:.4f} mmol/L")

line_x = np.linspace(0, 0.11, 100).reshape(-1, 1)
plt.scatter(X.ravel(), y, label="Standards")
plt.plot(line_x, model.predict(line_x), label="Regression")
plt.scatter([unknown_concentration], [unknown_absorbance], marker="X", s=120, label="Unknown")
plt.xlabel("Concentration (mmol/L)")
plt.ylabel("Absorbance")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()
