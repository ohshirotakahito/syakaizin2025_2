# -*- coding: utf-8 -*-
"""
演習：標準液の濃度と吸光度を可視化する（解説付き解答版）

【想定する場面】
分析装置の検量線を作るため、濃度が分かっている標準液を複数濃度で測定し、
吸光度を記録した。濃度と吸光度の関係がどれくらい直線的か（相関が強いか）
を確認し、散布図で可視化したい。

（課題）
1. 標準液の濃度と、それぞれの吸光度をNumPy配列として用意する。
2. 濃度と吸光度の相関係数を計算する。
3. 濃度と吸光度の関係を散布図で可視化する。
"""

import matplotlib.pyplot as plt
import numpy as np

# 標準液の濃度（mmol/L）と、それぞれを測定したときの吸光度です。
concentration = np.array([0.00, 0.02, 0.04, 0.06, 0.08, 0.10])
absorbance = np.array([0.01, 0.16, 0.31, 0.47, 0.61, 0.76])

# np.corrcoef(x, y) は、xとyの相関係数を計算し、2行2列の行列として返します。
# [0, 1]の位置（1行目2列目）が、xとyの間の相関係数そのものです。
# 相関係数は-1～1の範囲を取り、1に近いほど強い正の直線関係があることを表します。
correlation = np.corrcoef(concentration, absorbance)[0, 1]
print(f"濃度と吸光度の相関係数: {correlation:.4f}")

# plt.scatter() で、濃度を横軸、吸光度を縦軸とした散布図を描きます。
# 点の色(color)や大きさ(s)を指定すると、見やすいグラフになります。
plt.scatter(concentration, absorbance, color="#4C78A8", s=65)
plt.title("Calibration Standards")
plt.xlabel("Concentration (mmol/L)")
plt.ylabel("Absorbance")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()

# 【ポイント】
# ・相関係数が1に近いほど、点がほぼ一直線上に並ぶことを意味します。
# ・検量線としてこのデータを使う前に、まず散布図と相関係数で
#   「直線関係とみなせそうか」を確認するのが基本の流れです。
