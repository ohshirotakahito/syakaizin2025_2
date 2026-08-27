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

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# データセットの読み込み
data = pd.read_csv(DATA_DIR / "Solubility_Dataset.csv")

# 特徴とターゲットの分割
X = data.drop('Solubility', axis=1)
y = data['Solubility']

# 訓練セットとテストセットに分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

# StandardScalerと多層パーセプトロンをPipeline化します。
# early_stopping=Trueにより、検証性能が改善しなくなったら学習を止めます。
model = make_pipeline(
    StandardScaler(),
    MLPRegressor(hidden_layer_sizes=(64, 32), activation='relu',
                 early_stopping=True, max_iter=2000, random_state=42),
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f'Test MSE: {mse:.3f}')
print(f'Test R2: {r2:.3f}')

# 全テストデータについて実測値と予測値を比較します。
plt.figure(figsize=(7, 6))
plt.scatter(y_test, predictions, alpha=0.7)
lower = min(y_test.min(), predictions.min())
upper = max(y_test.max(), predictions.max())
plt.plot([lower, upper], [lower, upper], '--', color='red', label='Perfect prediction')
plt.xlabel('Actual Solubility')
plt.ylabel('Predicted Solubility')
plt.title('Solubility: Actual vs Predicted')
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()


