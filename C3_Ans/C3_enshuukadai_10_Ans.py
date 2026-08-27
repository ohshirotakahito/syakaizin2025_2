from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Sat Nov 18 00:19:54 2023

@author: toshiro
"""
# =============================================================================
# 10.機械学習(ディープニューラルネットワーク)を使用した新規材料の耐久度予測
# 背景
# 新型樹脂材料の開発において、耐久度の予測は重要な要素です。この演習では、深層学習を用いて、材料A、B、Cの異なる混合比率に基づいて、新規材料の耐久度を予測するモデルを構築します。
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
# 
# ータセット名 (material_science_dataset.csv, material_science_dataset1.csv, material_science_dataset2.csv, material_science_dataset3.csv)
# 
# 的
# ディープニューラルネットワークを使用して、材料A、B、Cの混合比率に基づいて新規材料の耐久度を予測する。
# 
# 手順
# データセットを読み込み、特徴量とターゲットを選択する。
# データを標準化し、訓練データとテストデータに分割する。
# ディープニューラルネットワークモデルを構築し、訓練する。
# モデルを評価し、平均二乗誤差（MSE）を計算する。
# 学習済みモデルとスケーラーを使用して、任意の混合比率から予測された耐久度を算出する。
# 期待される成果
# 混合比率に基づいた新規材料の耐久度の予測値。
# ディープニューラルネットワークを用いた耐久度予測モデルの構築と評価。
# =============================================================================

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# データセットの読み込み
df = pd.read_csv(DATA_DIR / "material_science_dataset1.csv")

# 特徴量とターゲットの選択
features = df.drop(['Existing_Durability_Years'], axis=1)
target = df['Existing_Durability_Years']

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=0
)

# 標準化とMLP回帰をつなぎ、学習データだけから前処理を学びます。
model = make_pipeline(
    StandardScaler(),
    MLPRegressor(hidden_layer_sizes=(64, 32), early_stopping=True,
                 max_iter=2000, random_state=42),
)
model.fit(X_train, y_train)
test_prediction = model.predict(X_test)
print(f"Mean Squared Error: {mean_squared_error(y_test, test_prediction):.3f}")
print(f"R2: {r2_score(y_test, test_prediction):.3f}")

def predict_durability(model, mixture_ratios, original_columns):
    # 混合比率を含むDataFrameを作成
    mixture_df = pd.DataFrame([mixture_ratios])

    # 残りの特徴量を平均値で埋める
    for col in original_columns:
        if col not in mixture_df.columns:
            mixture_df[col] = features[col].mean()

    # 特徴量の順序を訓練データと同じ順序にする
    mixture_df = mixture_df[original_columns]

    # 予測された耐久性を返す
    predicted_durability = model.predict(mixture_df)[0]
    return predicted_durability

# 例：材料の混合比率を入力して耐久度を予測
mixture_ratios = {'Mixture_Ratio_A_Percent': 10, 'Mixture_Ratio_B_Percent': 30, 'Mixture_Ratio_C_Percent': 30}

# 予測の際に元の特徴量の列名を渡す
predicted_durability = predict_durability(model, mixture_ratios, features.columns)
print(f"Predicted Durability: {predicted_durability:.2f} years")

