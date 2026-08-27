# -*- coding: utf-8 -*-
"""
演習：ニューラルネットワークを用いた化学データのパターン認識

【目的】
「Solubility」データセットを用いて、化合物の特性からその溶解度を予測する
ニューラルネットワークモデルを構築する。

【タスク】
1. データの読み込みと前処理。
2. ニューラルネットワークモデルの構築。
3. モデルの訓練。
4. モデルの評価と予測（MSE, R²）。
5. 結果の解析。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data_path = DATA_DIR / "Solubility_Dataset.csv"

if not data_path.exists():
    print(f"データが見つからないため、演習用の模擬データを作成します: {data_path}")
    data_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    n = 300
    molecular_weight = rng.uniform(50, 500, n)
    polarity = rng.uniform(0, 5, n)
    h_bond_donors = rng.integers(0, 5, n)
    h_bond_acceptors = rng.integers(0, 8, n)

    solubility = (
        2.0
        - 0.01 * molecular_weight
        + 0.6 * polarity
        + 0.3 * h_bond_donors
        + 0.2 * h_bond_acceptors
        + rng.normal(0, 0.5, n)
    )

    pd.DataFrame({
        "MolecularWeight": molecular_weight,
        "Polarity": polarity,
        "HBondDonors": h_bond_donors,
        "HBondAcceptors": h_bond_acceptors,
        "Solubility": solubility,
    }).to_csv(data_path, index=False)

data = pd.read_csv(data_path)

X = data.drop('Solubility', axis=1)
y = data['Solubility']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

# TODO: StandardScalerとMLPRegressorをmake_pipeline()で組み合わせ、学習させてください
# ヒント： MLPRegressor(hidden_layer_sizes=(64, 32), activation='relu',
#                      early_stopping=True, max_iter=2000, random_state=42)
model = None

# TODO: model.predict()でX_testを予測してください
predictions = np.full(len(y_test), y_train.mean())  # 仮実装（平均値で予測）

mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f'Test MSE: {mse:.3f}')
print(f'Test R2: {r2:.3f}')

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
