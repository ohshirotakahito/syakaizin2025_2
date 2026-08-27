# -*- coding: utf-8 -*-
"""
演習：設備振動の時系列を正常・異常へ分類する

【想定する場面】
設備の振動波形（120点の時系列）を、正常（label=0）と異常（label=1）に
分類するモデルを作る。異常時は基本周波数の2倍成分と大きなノイズが
加わる点を波形へ反映する。

※ 注意：ここで使うMLPClassifierは、時系列を1本の横長ベクトルとして
そのまま入力する全結合ニューラルネットワークです。LSTMなどの
再帰構造（RNN）は使っていません。「RNN」という呼び方をすることがありますが、
実際には時系列の並び自体は考慮しない点に注意してください。
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 正常・異常の模擬振動波形を作る
# =============================================================================

rng = np.random.default_rng(42)
time = np.linspace(0, 1, 120)
sequences = []
labels = []

for label in [0, 1]:
    for _ in range(250):
        frequency = rng.normal(12, 0.5)
        signal = np.sin(2 * np.pi * frequency * time + rng.uniform(0, 2 * np.pi))

        # TODO: labelが1（異常）なら2倍周波数成分と大きなノイズ（標準偏差0.25）を、
        #       labelが0（正常）なら小さなノイズ（標準偏差0.08）をsignalへ加えてください
        # ヒント：
        #   if label:
        #       signal += 0.6 * np.sin(2 * np.pi * frequency * 2 * time) + rng.normal(0, 0.25, time.size)
        #   else:
        #       signal += rng.normal(0, 0.08, time.size)

        sequences.append(signal)
        labels.append(label)

X = np.asarray(sequences)
y = np.asarray(labels)


# =============================================================================
# 2. 学習用とテスト用に分ける
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)


# =============================================================================
# 3. 標準化とMLPClassifierを組み合わせて学習する
# =============================================================================

# TODO: StandardScalerとMLPClassifierをmake_pipeline()で組み合わせ、学習させてください
# ヒント： MLPClassifier(hidden_layer_sizes=(48,), early_stopping=True,
#                       max_iter=1000, random_state=42)
model = None

# TODO: model.predict()でX_testを分類してください
pred = None


# =============================================================================
# 4. 分類結果を評価する
# =============================================================================

print(classification_report(y_test, pred, target_names=["Normal", "Fault"]))

ConfusionMatrixDisplay.from_predictions(
    y_test, pred, display_labels=["Normal", "Fault"], cmap="Blues"
)
plt.title("Motor Vibration Classification")
plt.tight_layout()
plt.show()
