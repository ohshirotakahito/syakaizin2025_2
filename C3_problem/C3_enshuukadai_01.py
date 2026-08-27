# -*- coding: utf-8 -*-
"""
演習：汚染物質の濃度と影響を分析する線形回帰モデルを構築する

（演習課題）
汚染物質の濃度と影響を分析するための線形回帰モデルを構築し、評価する。

手順：
1. データセットを訓練データとテストデータに分割する。
2. LinearRegressionモデルを使用して訓練データに適合させる。
3. モデルをテストデータで評価し、平均二乗誤差（MSE）と決定係数（R²）を計算する。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

csv_file_path = DATA_DIR / "pollutant_concentration_effect_data.csv"

if not csv_file_path.exists():
    print(f"データが見つからないため、演習用の模擬データを作成します: {csv_file_path}")
    csv_file_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    concentration = rng.uniform(0, 100, 200)
    effect = 5 + 0.75 * concentration + rng.normal(0, 6, concentration.size)

    pd.DataFrame({
        "Pollutant Concentration": concentration,
        "Effect": effect,
    }).to_csv(csv_file_path, index=False)

data = pd.read_csv(csv_file_path)

X = data[['Pollutant Concentration']]
y = data['Effect']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = LinearRegression()

# TODO: modelをX_train, y_trainで学習させてください
# ヒント： model.fit(X_train, y_train)

x_range = np.linspace(X.min(), X.max(), 100)

# TODO: x_rangeに対する予測値y_rangeを求めてください
# ヒント： model.predict(x_range)
# 未学習の間はx_rangeと同じ形のゼロ配列にしておきます。
y_range = np.zeros(len(x_range))

plt.scatter(data['Pollutant Concentration'], data['Effect'], label='Data')
plt.plot(x_range, y_range, color='red', label='Regression Line')
plt.xlabel('Pollutant Concentration')
plt.ylabel('Effect')
plt.title('Pollutant Concentration vs Effect')
plt.legend()
plt.show()

# TODO: X_testに対する予測値y_predを求め、MSEとR2を計算してください
# ヒント： y_pred = model.predict(X_test)
#         mean_squared_error(y_test, y_pred)
#         r2_score(y_test, y_pred)
y_pred = np.zeros(len(y_test))
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.3f}")
print(f"R2: {r2:.3f}")
