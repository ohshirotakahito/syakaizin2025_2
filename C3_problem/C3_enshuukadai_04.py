# -*- coding: utf-8 -*-
"""
演習：反応物の濃度の時間変化から反応速度を求める

（課題）
三種類の物質A、B、Cが時間と共に変化する化学反応（A + B → C）に関する
時系列データを用いて、濃度の時間変化をプロットし、反応速度を計算する。

反応速度の定義：反応速度 = −Δ[A] / Δt

※ このファイルはTODOを埋める前でも最後まで実行できます（反応速度は0と表示されます）。
"""

import numpy as np
import matplotlib.pyplot as plt

time = np.array([0, 5, 10, 15, 20])
conc_A = np.array([1.00, 0.80, 0.64, 0.51, 0.41])
conc_B = np.array([1.00, 0.80, 0.64, 0.51, 0.41])
conc_C = np.array([0.00, 0.20, 0.36, 0.49, 0.59])

plt.plot(time, conc_A, label='Concentration of A', marker='o')
plt.plot(time, conc_B, label='Concentration of B', marker='o')
plt.plot(time, conc_C, label='Concentration of C', marker='o')
plt.xlabel('Time (minutes)')
plt.ylabel('Concentration (M)')
plt.title('Concentration Changes Over Time')
plt.legend()
plt.show()

# TODO: np.diff()を使って、conc_A, conc_B, conc_C, timeの
#       隣り合う値どうしの差(delta_conc_A など)を求めてください
# ヒント： np.diff(conc_A)
delta_conc_A = np.zeros(len(conc_A) - 1)
delta_conc_B = np.zeros(len(conc_B) - 1)
delta_conc_C = np.zeros(len(conc_C) - 1)
delta_time = np.diff(time)

# TODO: 反応物A, Bは-delta_conc/delta_time、生成物Cはdelta_conc/delta_timeで
#       反応速度を求めてください
reaction_rate_A = -delta_conc_A / delta_time
reaction_rate_B = -delta_conc_B / delta_time
reaction_rate_C = delta_conc_C / delta_time

average_rate_A = np.mean(reaction_rate_A)
average_rate_B = np.mean(reaction_rate_B)
average_rate_C = np.mean(reaction_rate_C)

print("Aの平均反応速度:", average_rate_A, "M/分")
print("Bの平均反応速度:", average_rate_B, "M/分")
print("Cの平均反応速度:", average_rate_C, "M/分")
