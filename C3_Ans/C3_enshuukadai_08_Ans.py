from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Fri Nov 17 11:39:34 2023

@author: ohshi
"""
# =============================================================================
# ７．ニューラルネットワークを用いた化学データのパターン認識
# 
# 目的
# 生成された「Solubility」データセットを用いて、化合物の特性からその溶解度を予測するニューラルネットワークモデルを構築する。
# 深層学習の基本的な概念を理解し、実際のデータに適用する。
# データセット
# 「Solubility」データセットには、化合物の分子量、極性、水素結合ドナー数、水素結合アクセプター数、および溶解度が含まれています。
# データはCSV形式で提供されます。
# タスク
# データの読み込みと前処理：
# 
# Pandasを使用してCSVファイルからデータセットを読み込みます。
# 特徴（分子量、極性など）とターゲット（溶解度）にデータを分割します。
# データの正規化または標準化を行うことを検討します。
# ニューラルネットワークモデルの構築：
# 
# KerasやTensorFlowなどのライブラリを使用してニューラルネットワークモデルを構築します。
# 少なくとも一つの隠れ層を持つシンプルなモデルから始めます。
# 損失関数と最適化アルゴリズムを選択し、モデルをコンパイルします。
# モデルの訓練：
# 
# データを訓練セットとテストセットに分割します。
# ニューラルネットワークを訓練セットで訓練し、適切なエポック数とバッチサイズを選択します。
# モデルの評価と予測：
# 
# テストセットを使用してモデルの性能を評価します。
# 精度と損失を計算し、モデルの予測能力を確認します。
# 結果の解析：
# 
# 訓練とテストの結果を分析し、モデルの改善点を特定します。
# モデルが化学データのパターンをどの程度正しく認識しているかを考察します。
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データの読み込み
data_a = pd.read_csv(DATA_DIR / "Vibration_Data_Wall_A.csv")
data_b = pd.read_csv(DATA_DIR / "Vibration_Data_Wall_B.csv")

# フーリエ変換関数の定義（変更なし）
def perform_fft(data):
    n = len(data)
    fft_data = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(n, d=1/n)
    return fft_data[:n // 2], fft_freq[:n // 2]  # 正の周波数のみを対象

# 壁Aのデータに対するフーリエ変換
fft_a, freq_a = perform_fft(data_a['Vibration'])

# 壁Bのデータに対するフーリエ変換
fft_b, freq_b = perform_fft(data_b['Vibration'])

# 結果のプロット（改善版）
plt.figure(figsize=(8, 6))
plt.plot(freq_a, np.abs(fft_a), label='Wall A')
plt.plot(freq_b, np.abs(fft_b), label='Wall B')
plt.title('Frequency Spectrum of Wall A and B')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.legend()
plt.show()



