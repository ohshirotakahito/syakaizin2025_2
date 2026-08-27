# -*- coding: utf-8 -*-
"""
演習：センサーの過去24点から次時点の値を予測する

【想定する場面】
周期的な変動とゆるやかな上昇傾向（ドリフト）を持つセンサー温度の時系列
データについて、直近24点の値から次の1点を予測するモデルを作る。

※ 注意：ここで使うMLPRegressorは、直近24点を1本の横長ベクトルとして
入力する全結合ニューラルネットワークです。LSTMなどの再帰構造（RNN）は
使っていません。「過去の窓（ウィンドウ）を特徴量として使う」という
古典的な時系列予測の手法です。
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 模擬センサーデータを作る
# =============================================================================

rng = np.random.default_rng(42)
t = np.arange(1200)
signal = 20 + 2 * np.sin(2 * np.pi * t / 96) + 0.003 * t + rng.normal(0, 0.25, t.size)


# =============================================================================
# 2. 過去24点を特徴量、次の1点を正解とする学習データを作る
# =============================================================================

window = 24
X = []
y = []

# TODO: indexをwindowからlen(signal)まで動かし、
#       signal[index-window:index]をX、signal[index]をyへ追加してください
for index in range(window, len(signal)):
    pass

X = np.asarray(X)
y = np.asarray(y)


# =============================================================================
# 3. 前半80%を学習データ、後半20%をテストデータにする
# =============================================================================

split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


# =============================================================================
# 4. 標準化とMLPRegressorを組み合わせて学習する
# =============================================================================

# TODO: StandardScalerとMLPRegressorをmake_pipeline()で組み合わせ、学習させてください
# ヒント： MLPRegressor(hidden_layer_sizes=(32,), early_stopping=True,
#                      max_iter=1000, random_state=42)
model = None

# TODO: model.predict()でX_testを予測してください
pred = None


# =============================================================================
# 5. 予測性能を確認する
# =============================================================================

print(f"時系列テストMAE: {mean_absolute_error(y_test, pred):.3f}")

plt.plot(y_test[:180], label="Actual")
plt.plot(pred[:180], label="Predicted")
plt.title("Next-step Sensor Forecast")
plt.xlabel("Test time step")
plt.ylabel("Temperature")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
