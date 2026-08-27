from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
# =============================================================================
# １５．スペクトルのピーク検出
# 
# 質量分析のスペクトルです．シグナルのピークを，m/zと強度をテーブル表にしたいと思います．
# スペクトルにはノイズがありますが，ノイズではないシグナルを抽出したい．
# data/MS_spectrum_data.csv'
# =============================================================================


import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

# ファイルパス
file_path = DATA_DIR / "MS_spectrum_data.csv"

# CSVファイルの読み込み
spectrum_data = pd.read_csv(file_path)

# データの先頭部分を表示して内容を確認
spectrum_data.head()

# m/z と Intensity の値でプロットを作成
plt.figure(figsize=(12, 6))
plt.plot(spectrum_data['m/z'], spectrum_data['Intensity'])
plt.title('Mass Spectrum')
plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.grid(True)
plt.show()

# m/zの範囲を決定
mz_min = spectrum_data['m/z'].min()
mz_max = spectrum_data['m/z'].max()

# m/zの範囲を100分割するための分割点を計算
mz_bins = np.linspace(mz_min, mz_max, num=101)

# 各分割領域でのIntensityの標準偏差を計算
std_deviations = []
for i in range(100):
    # 各ビンに含まれるIntensity値を取得
    bin_intensity = spectrum_data[(spectrum_data['m/z'] >= mz_bins[i]) & (spectrum_data['m/z'] < mz_bins[i+1])]['Intensity']
    # 標準偏差を計算
    std_deviations.append(bin_intensity.std(ddof=0))

# 標準偏差の平均値を計算
mean_std_deviation = np.mean(std_deviations)

# ノイズ除去の閾値を設定（平均値の3倍）
noise_threshold = 3 * mean_std_deviation

# 閾値を超えるピークを検出
peaks_filtered, _ = find_peaks(spectrum_data['Intensity'], height=noise_threshold)

# フィルタリングされたピークのm/zとIntensity値を抽出
peak_mz_filtered = spectrum_data['m/z'].iloc[peaks_filtered]
peak_intensity_filtered = spectrum_data['Intensity'].iloc[peaks_filtered]

# フィルタリングされたピークデータをDataFrameに格納
peak_data_filtered = pd.DataFrame({'m/z': peak_mz_filtered, 'Intensity': peak_intensity_filtered})

# ピークデータをCSVに保存
output_file_path_filtered = DATA_DIR / "MS_spectrum_peaks_filtered.csv"
peak_data_filtered.to_csv(output_file_path_filtered, index=False)

# ピークデータを表示
print(peak_data_filtered)
