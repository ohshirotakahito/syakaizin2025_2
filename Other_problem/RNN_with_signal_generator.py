# -*- coding: utf-8 -*-
"""
演習：周期・ドリフト・ノイズを含むポンプ圧力の次時点予測

【想定する場面】
2つの周期成分とゆるやかな上昇傾向（ドリフト）、測定ノイズを含む
ポンプ圧力の時系列データについて、直近40点の値から次の1点を予測する
モデルを作り、予測誤差と残差（実測値−予測値）を確認する。

※ 注意：ここで使うMLPRegressorは、直近40点を1本の横長ベクトルとして
入力する全結合ニューラルネットワークです。LSTMなどの再帰構造（RNN）は
使っていません。
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 模擬ポンプ圧力データを作る
# =============================================================================

rng = np.random.default_rng(7)
t = np.arange(1800)
pressure = (
    210
    + 10 * np.sin(2 * np.pi * t / 80)
    + 4 * np.sin(2 * np.pi * t / 17)
    + 0.004 * t
    + rng.normal(0, 1.2, t.size)
)


# =============================================================================
# 2. 過去40点を特徴量、次の1点を正解とする学習データを作る
# =============================================================================

window = 40

# TODO: pressureから、直近window点を1行とする特徴量Xと、
#       その次の値を正解とする配列yを作ってください
# ヒント： X = np.asarray([pressure[i-window:i] for i in range(window, len(pressure))])
#         y = pressure[window:]
X = None
y = None


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
# ヒント： MLPRegressor(hidden_layer_sizes=(48, 24), early_stopping=True,
#                      max_iter=1200, random_state=42)
model = None

# TODO: model.predict()でX_testを予測してください
pred = None


# =============================================================================
# 5. 予測誤差と残差を確認する
# =============================================================================

print(f"Test RMSE: {np.sqrt(mean_squared_error(y_test, pred)):.2f} kPa")

fig, axes = plt.subplots(2, 1, figsize=(10, 7))
axes[0].plot(y_test[:200], label="Actual")
axes[0].plot(pred[:200], label="Predicted")
axes[0].legend()
axes[0].set_ylabel("kPa")

axes[1].scatter(pred, y_test - pred, alpha=0.5)
axes[1].axhline(0, color="red", linestyle="--")
axes[1].set(xlabel="Predicted kPa", ylabel="Residual")

fig.tight_layout()
plt.show()
