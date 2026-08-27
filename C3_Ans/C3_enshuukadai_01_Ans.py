from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
# =============================================================================
# １．線形回帰モデルの構築:汚染物質の濃度と影響を分析する
# 
# （演習課題）汚染物質の濃度と影響を分析するための線形回帰モデルを構築し、評価する。
# データ: 以下のデータ（Pollutant Concentration.csv）を用います。
# 
# 汚染物質の濃度（0ppmから100ppmの範囲）
# 計測値は濃度に比例しているが，測定誤差や環境要因によりランダムなノイズが加わっていると考えられる．手順は以下を行ってください．
# データセットを訓練データとテストデータに分割します。
# LinearRegressionモデルを使用して訓練データに適合させます。
# モデルをテストデータで評価し、平均二乗誤差（MSE）と決定係数（R²）を計算します。
# =============================================================================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# CSVファイルの読み込み
csv_file_path = DATA_DIR / "pollutant_concentration_effect_data.csv"
data = pd.read_csv(csv_file_path)

# データセットを訓練セットとテストセットに分割
X = data[['Pollutant Concentration']]
y = data['Effect']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 線形回帰モデルの構築
model = LinearRegression()
model.fit(X_train, y_train)

# 回帰直線の描画のための準備
x_range = np.linspace(X.min(), X.max(), 100)
y_range = model.predict(x_range)

# データと回帰直線のプロット
plt.scatter(data['Pollutant Concentration'], data['Effect'], label='Data')
plt.plot(x_range, y_range, color='red', label='Regression Line')
plt.xlabel('Pollutant Concentration')
plt.ylabel('Effect')
plt.title('Pollutant Concentration vs Effect')
plt.legend()
plt.show()

# モデルの評価
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(mse, r2)

