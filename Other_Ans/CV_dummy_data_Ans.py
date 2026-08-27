# -*- coding: utf-8 -*-
# 解答版：現実的な利用場面、処理の意味、結果の限界を確認します。
"""
Created on Fri Nov  3 02:13:39 2023

@author: toshiro
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

# 電位の範囲を定義
E = np.linspace(E_start, E_end, 1000)
E = np.concatenate([E, np.flip(E)])

# 酸化電流と還元電流のピークをシミュレート
I_oxidation = peak_current * np.exp(-(E - E_peak)**2 / (2 * peak_width**2))
I_reduction = peak_current * np.exp(-(E + E_peak)**2 / (2 * peak_width**2))

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
