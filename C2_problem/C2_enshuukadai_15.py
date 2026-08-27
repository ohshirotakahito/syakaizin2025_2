# -*- coding: utf-8 -*-
"""
演習：質量スペクトルからノイズを除いたピークを検出する

（課題）
質量分析のスペクトルです。シグナルのピークを、m/zと強度をテーブル表に
したいと思います。スペクトルにはノイズがありますが、ノイズではない
シグナルを抽出したい。
data/MS_spectrum_data.csv

※ このファイルはTODOを埋める前でも最後まで実行できます
   （しきい値を非常に高く設定してあるため、ピークは検出されません）。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

file_path = DATA_DIR / "MS_spectrum_data.csv"

if not file_path.exists():
    print(f"スペクトルデータが見つからないため、演習用の模擬データを作成します: {file_path}")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    mz = np.linspace(50, 500, 2251)
    intensity = np.full_like(mz, 20.0)

    sample_peaks = [(91.1, 400, 0.4), (149.0, 700, 0.5), (279.2, 550, 0.6), (350.2, 900, 0.4)]
    for center, height, width in sample_peaks:
        intensity += height * np.exp(-((mz - center) ** 2) / (2 * width ** 2))
    intensity = np.clip(intensity + rng.normal(0, 10, mz.size), 0, None)

    pd.DataFrame({"m/z": mz, "Intensity": intensity}).to_csv(file_path, index=False)

spectrum_data = pd.read_csv(file_path)
print(spectrum_data.head())

plt.figure(figsize=(12, 6))
plt.plot(spectrum_data['m/z'], spectrum_data['Intensity'])
plt.title('Mass Spectrum')
plt.xlabel('m/z')
plt.ylabel('Intensity')
plt.grid(True)
plt.show()

mz_min = spectrum_data['m/z'].min()
mz_max = spectrum_data['m/z'].max()
mz_bins = np.linspace(mz_min, mz_max, num=101)

# TODO: 各ビン(区間)ごとにIntensityの標準偏差を求め、std_deviationsに追加してください
# ヒント： bin_intensity = spectrum_data[
#             (spectrum_data['m/z'] >= mz_bins[i]) & (spectrum_data['m/z'] < mz_bins[i + 1])
#         ]['Intensity']
#         std_deviations.append(bin_intensity.std(ddof=0))
std_deviations = []
for i in range(100):
    pass

# TODO: std_deviationsの平均を求め、その3倍をnoise_thresholdとしてください
# ヒント： mean_std_deviation = np.mean(std_deviations)
#         noise_threshold = 3 * mean_std_deviation
# 未実装の間は、しきい値をIntensityの最大値より大きくしておき、
# ピークが1つも検出されないようにしています。
noise_threshold = spectrum_data['Intensity'].max() + 1

peaks_filtered, _ = find_peaks(spectrum_data['Intensity'], height=noise_threshold)

peak_mz_filtered = spectrum_data['m/z'].iloc[peaks_filtered]
peak_intensity_filtered = spectrum_data['Intensity'].iloc[peaks_filtered]

peak_data_filtered = pd.DataFrame({'m/z': peak_mz_filtered, 'Intensity': peak_intensity_filtered})

output_file_path_filtered = DATA_DIR / "MS_spectrum_peaks_filtered.csv"
peak_data_filtered.to_csv(output_file_path_filtered, index=False)

print("\n【検出されたピーク】")
print(peak_data_filtered)
print(f"\nノイズしきい値: {noise_threshold:.1f}")
print(f"保存先: {output_file_path_filtered}")
