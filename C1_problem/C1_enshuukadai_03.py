# -*- coding: utf-8 -*-
"""
演習：標準液の濃度と吸光度を可視化する

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

concentration = np.array([0.00, 0.02, 0.04, 0.06, 0.08, 0.10])
absorbance = np.array([0.01, 0.16, 0.31, 0.47, 0.61, 0.76])

# TODO: concentrationとabsorbanceの相関係数を求めてください
# ヒント： np.corrcoef(concentration, absorbance)[0, 1]
correlation = None

print(f"濃度と吸光度の相関係数: {correlation:.4f}")

# TODO: concentrationを横軸、absorbanceを縦軸とした散布図を描いてください
# ヒント： plt.scatter(concentration, absorbance, color="#4C78A8", s=65)

plt.title("Calibration Standards")
plt.xlabel("Concentration (mmol/L)")
plt.ylabel("Absorbance")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()
