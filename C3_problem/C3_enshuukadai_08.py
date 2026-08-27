# -*- coding: utf-8 -*-
"""
演習：壁の振動データをフーリエ変換して周波数成分を比較する

【想定する場面】
建物の壁A・壁Bそれぞれで振動センサーによる時系列データを記録した。
振動が「どの周波数成分を多く含むか」を比較するため、フーリエ変換
（FFT）を使って時間領域のデータを周波数領域のデータへ変換する。

（課題）
1. 壁A・壁Bの振動データをそれぞれ読み込む。
2. 各データに離散フーリエ変換（DFT/FFT）を適用し、周波数ごとの
   振幅（強さ）を求める関数を作成する。
3. 壁A・壁Bの周波数スペクトルを1つのグラフに重ねて表示し、比較する。

※ このファイルはTODOを埋める前でも最後まで実行できます（スペクトルは全て0になります）。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path_a = DATA_DIR / "Vibration_Data_Wall_A.csv"
data_path_b = DATA_DIR / "Vibration_Data_Wall_B.csv"

if not (data_path_a.exists() and data_path_b.exists()):
    print("振動データが見つからないため、演習用の模擬データを作成します。")
    data_path_a.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    n_samples = 500
    t = np.arange(n_samples)

    vibration_a = np.sin(2 * np.pi * 5 * t / n_samples) + rng.normal(0, 0.2, n_samples)
    vibration_b = np.sin(2 * np.pi * 15 * t / n_samples) + rng.normal(0, 0.2, n_samples)

    pd.DataFrame({"Time": t, "Vibration": vibration_a}).to_csv(data_path_a, index=False)
    pd.DataFrame({"Time": t, "Vibration": vibration_b}).to_csv(data_path_b, index=False)

data_a = pd.read_csv(data_path_a)
data_b = pd.read_csv(data_path_b)


def perform_fft(data):
    """時系列データにフーリエ変換を適用し、正の周波数成分だけを返す。"""
    n = len(data)

    # TODO: np.fft.fft(data)でfft_dataを求めてください
    fft_data = np.zeros(n, dtype=complex)

    # TODO: np.fft.fftfreq(n, d=1/n)でfft_freqを求めてください
    fft_freq = np.zeros(n)

    return fft_data[:n // 2], fft_freq[:n // 2]


fft_a, freq_a = perform_fft(data_a['Vibration'])
fft_b, freq_b = perform_fft(data_b['Vibration'])

plt.figure(figsize=(8, 6))
plt.plot(freq_a, np.abs(fft_a), label='Wall A')
plt.plot(freq_b, np.abs(fft_b), label='Wall B')
plt.title('Frequency Spectrum of Wall A and B')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
