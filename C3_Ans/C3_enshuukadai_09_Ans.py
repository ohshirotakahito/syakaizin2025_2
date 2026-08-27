from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Fri Nov 17 23:53:21 2023

@author: toshiro
"""
# =============================================================================
# 9.機械学習(ランダムフォレス)を使用した新規材料の耐久度予測
# 背景
# 新型樹脂材料の開発において、耐久度を最大化することが重要な課題です。この演習では、材料A、B、Cの3つの異なる成分が材料の特性に与える影響を理解し、任意の混合比率で材料の耐久度を予想できるように機械学習モデルを構築します。
# 
# データセット
# 提供されるデータセットには、以下の情報が含まれます：
# 
# 既存材料の耐久性 (年)
# 材料A、B、Cの混合比率 (%)
# 引張強度 (MPa)
# 熱耐性 (°C)
# 弾性率 (GPa)
# 硬度 (モース硬度)
# 耐食性 (スケール1-10)
# 電気伝導率 (S/m)
# 密度 (g/cm^3)
# 目的
# 材料A、B、Cの任意の混合比率に基づいて新規材料の耐久度を予測します。
# 
# ータセット名 (material_science_dataset.csv, material_science_dataset1.csv, material_science_dataset2.csv, material_science_dataset3.csv)
# 
# 手順
# データセットを分析し、各特性が耐久性にどのように影響するかを理解する。
# 機械学習モデル（ランダムフォレスト）を使用して、耐久性に影響を与える主要な因子を特定し、モデルを訓練する。
# 最適化アルゴリズムを使用して、耐久性を最大化する材料の混合比率を求める。
# 最適な混合比率を用いて、新規材料の耐久度を予測する。
# =============================================================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from scipy.optimize import minimize

# データセットの読み込み
df = pd.read_csv(DATA_DIR / "material_science_dataset1.csv")

# 特徴量とターゲットの選択
features = df.drop(['Existing_Durability_Years'], axis=1)
target = df['Existing_Durability_Years']

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)

# モデルの訓練
model = RandomForestRegressor(random_state=0)
model.fit(X_train, y_train)

# モデルの評価
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# 最適な混合比率を求める関数
def optimize_mixture_ratio(x):
    # 混合比率を保持するDataFrameを作成
    mixture_df = pd.DataFrame([x], columns=['Mixture_Ratio_A_Percent', 'Mixture_Ratio_B_Percent', 'Mixture_Ratio_C_Percent'])
    # 残りの特徴量を平均値で埋める
    for col in features.columns:
        if col not in mixture_df.columns:
            mixture_df[col] = features[col].mean()
    # 学習時と同じ列順にそろえます。列名が同じでも順序違いは予測エラーになります。
    mixture_df = mixture_df[features.columns]
    # 予測された耐久性を返す
    return -model.predict(mixture_df)[0]  # 耐久性を最大化するためにマイナスを使用

# 制約条件（混合比率の合計が100%）
constraints = ({'type': 'eq', 'fun': lambda x: 100 - sum(x)})

# 最適化の実行
initial_guess = [10, 10, 10]
result = minimize(optimize_mixture_ratio, initial_guess, constraints=constraints, bounds=[(0,100), (0,100), (0,100)])
optimal_mixture = result.x

# 最適な混合比率に基づく耐久性の予測
optimal_mixture_df = pd.DataFrame([optimal_mixture], columns=['Mixture_Ratio_A_Percent', 'Mixture_Ratio_B_Percent', 'Mixture_Ratio_C_Percent'])
for col in features.columns:
    if col not in optimal_mixture_df.columns:
        optimal_mixture_df[col] = features[col].mean()
optimal_mixture_df = optimal_mixture_df[features.columns]
predicted_durability = model.predict(optimal_mixture_df)[0]

print(f"Optimal Mixture Ratios: A: {optimal_mixture[0]:.2f}%, B: {optimal_mixture[1]:.2f}%, C: {optimal_mixture[2]:.2f}%")
print(f"Predicted Durability: {predicted_durability:.2f} years")
