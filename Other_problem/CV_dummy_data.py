# -*- coding: utf-8 -*-
"""
演習：サイクリックボルタモグラムの模擬データを作る

CV（サイクリックボルタンメトリー）では、電極へ加える電位を往復させ、
そのとき流れる電流を記録します。物質が酸化・還元される付近では、
電流が山または谷のように変化します。
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# パラメータ設定
E_start = -1.0
E_end = 1.0
E_peak = 0.5
E_half_peak = 0.25
peak_width = 0.1
scan_rate = 0.1
current_baseline = 1e-6
peak_current = 5e-6

# 電位の範囲を定義（往路と復路をつなげる）
E = np.linspace(E_start, E_end, 1000)
E = np.concatenate([E, np.flip(E)])

# TODO: 酸化電流のピーク（E_peak付近が最大になる釣鐘型）を作ってください
# ヒント： peak_current * np.exp(-(E - E_peak)**2 / (2 * peak_width**2))
I_oxidation = None

# TODO: 還元電流のピーク（-E_peak付近が最大になる釣鐘型）を作ってください
# ヒント： peak_current * np.exp(-(E + E_peak)**2 / (2 * peak_width**2))
I_reduction = None

# 酸化電流と還元電流を合成
I = I_oxidation - I_reduction + current_baseline

# プロット
plt.plot(E, I)
plt.xlabel('Potential (V)')
plt.ylabel('Current (A)')
plt.title('Simulated Cyclic Voltammogram')
plt.grid(True)
plt.show()

# データをDataFrameに変換
#data = pd.DataFrame({'Potential': E, 'Current': I})

# CSVファイルに保存
#data.to_csv('cyclic_voltammetry_data.csv', index=False)
