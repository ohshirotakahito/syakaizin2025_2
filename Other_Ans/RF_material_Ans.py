from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：現実的な利用場面、処理の意味、結果の限界を確認します。
"""
Created on Fri Nov 17 23:53:21 2023

@author: toshiro
"""
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
