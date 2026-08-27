# -*- coding: utf-8 -*-
"""
演習：吸光度の検量線から未知試料濃度を推定する（解説付き解答版）

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

# 標準液の濃度（説明変数）です。
# LinearRegressionは「1行1サンプル、1列1特徴量」の2次元配列を入力に求めるため、
# reshape(-1, 1) で6行1列の形に変換しています。
X = np.array([0.00, 0.02, 0.04, 0.06, 0.08, 0.10]).reshape(-1, 1)

# 標準液の吸光度（目的変数）です。
y = np.array([0.01, 0.16, 0.31, 0.47, 0.61, 0.76])

# LinearRegression().fit(X, y) で、Xとyの関係を最もよく表す直線
# 「y = 傾き × X + 切片」の傾きと切片を求めます（最小二乗法）。
model = LinearRegression().fit(X, y)

# 濃度が分からない未知試料の吸光度です。
unknown_absorbance = 0.40

# 検量線の式 Abs = coef * C + intercept を、Cについて解くと
# C = (Abs - intercept) / coef になります。この式を使って、
# 吸光度から逆に濃度を推定します。
unknown_concentration = (unknown_absorbance - model.intercept_) / model.coef_[0]

print(f"検量線: Abs={model.coef_[0]:.3f}*C+{model.intercept_:.3f}")
print(f"吸光度{unknown_absorbance:.2f}の推定濃度: {unknown_concentration:.4f} mmol/L")

# グラフ表示用に、0～0.11の範囲を100点に区切った直線描画用のx座標を作ります。
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

# 【ポイント】
# ・検量線は「濃度→吸光度」を予測する式ですが、実務では逆に
#   「吸光度→濃度」を知りたいことが多いため、式を変形して使います。
# ・未知試料の吸光度が標準液の測定範囲（0.01～0.76）から大きく外れる場合、
#   その外側での推定精度は保証されない点に注意が必要です。
