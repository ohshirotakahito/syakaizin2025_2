# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Fri Nov 17 11:21:02 2023

@author: ohshi
"""
# =============================================================================
# ４．時系列データ分析:　反応物の濃度から反応速度を求める
# 三種類の物質A、B、Cが時間と共に変化する化学反応に関する時系列データを作成し、
# そのデータを基にプロット作成と反応速度の計算を行う問題です。
# 
# 反応式
# 考えられる反応式は次のようになります：A+B→C
# 
# 時系列データ
# 以下の表は、反応物A、Bと生成物Cの濃度を時間の経過と共に記録したものです（時間は分、濃度はモル/リットル（M））：
# 
# 時間 (分)	Aの濃度 (M)	Bの濃度 (M)	Cの濃度 (M)
# 0	1.00	1.00	0.00
# 5	0.80	0.80	0.20
# 10	0.64	0.64	0.36
# 15	0.51	0.51	0.49
# 20	0.41	0.41	0.59
# 問題
# 上記のデータを用いて、反応物A、B、および生成物Cの濃度の時間変化をプロットしてください。
# 反応速度を計算してください。反応速度は、反応物AまたはBの濃度の時間に対する変化率で求めることができます。この反応では、AとBが同じモル比で反応していると仮定します。
# 解法ヒント
# 反応速度は次のように定義されます：
# 反応速度=−Δ[A]/Δt
# ここで、Δ[X]は物質Xの濃度の変化、
# Δtはその変化が起きた時間の差です。反応物AとBの濃度が減少しているので、反応速度の式には負の符号がついています。
# 
# この問題では、時間ごとの濃度の変化を計算し、その結果をプロットし、
# 平均反応速度を求めることで問題を解決できます。
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# 時間（分）と物質の濃度（M）のデータ
time = np.array([0, 5, 10, 15, 20])  # 時間 (分)
conc_A = np.array([1.00, 0.80, 0.64, 0.51, 0.41])  # Aの濃度 (M)
conc_B = np.array([1.00, 0.80, 0.64, 0.51, 0.41])  # Bの濃度 (M)
conc_C = np.array([0.00, 0.20, 0.36, 0.49, 0.59])  # Cの濃度 (M)

# 濃度のプロット
plt.plot(time, conc_A, label='Concentration of A', marker='o')
plt.plot(time, conc_B, label='Concentration of B', marker='o')
plt.plot(time, conc_C, label='Concentration of C', marker='o')
plt.xlabel('Time (minutes)')
plt.ylabel('Concentration (M)')
plt.title('Concentration Changes Over Time')
plt.legend()
plt.show()

# 濃度の変化と時間の変化を計算
delta_conc_A = np.diff(conc_A)  # Aの濃度の変化
delta_conc_B = np.diff(conc_B)  # Bの濃度の変化
delta_conc_C = np.diff(conc_C)  # Cの濃度の変化
delta_time = np.diff(time)  # 時間の変化

# 反応速度を計算（反応物は負の値、生成物は正の値を取る）
reaction_rate_A = -delta_conc_A / delta_time
reaction_rate_B = -delta_conc_B / delta_time
reaction_rate_C = delta_conc_C / delta_time

# 反応速度の平均値を計算
average_rate_A = np.mean(reaction_rate_A)
average_rate_B = np.mean(reaction_rate_B)
average_rate_C = np.mean(reaction_rate_C)

print("Aの平均反応速度:", average_rate_A, "M/分")
print("Bの平均反応速度:", average_rate_B, "M/分")
print("Cの平均反応速度:", average_rate_C, "M/分")
