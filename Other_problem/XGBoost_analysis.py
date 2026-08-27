# -*- coding: utf-8 -*-
"""
演習：不均衡な設備故障データを勾配ブースティングで分類する

【想定する場面】
設備の温度・振動・整備間隔・負荷から、故障（少数派クラス）を予測する。
故障データは全体のごく一部しかないため、少数派クラスへ大きな重みを付け、
判定しきい値も業務目的に合わせて調整する。

※ 注意：ここではscikit-learnの HistGradientBoostingClassifier を使います。
xgboostライブラリ自体は使用していませんが、勾配ブースティングという
考え方（弱い決定木を順番に足し合わせて精度を上げる）は共通です。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split


# =============================================================================
# 1. 模擬の設備データと故障ラベルを作る
# =============================================================================

rng = np.random.default_rng(42)
n = 2400

temperature = rng.normal(68, 8, n)
vibration = rng.gamma(2, 1.2, n)
maintenance_hours = rng.integers(0, 1800, n)
load = rng.normal(75, 15, n)

# 各要因が故障確率へ与える影響をロジスティック関数で表します。
score = (
    -5.2
    + 0.07 * (temperature - 68)
    + 0.5 * (vibration - 2.4)
    + 0.0018 * (maintenance_hours - 700)
    + 0.025 * (load - 75)
)
probability = 1 / (1 + np.exp(-score))
failure = rng.binomial(1, probability)

data = pd.DataFrame({
    "temperature": temperature,
    "vibration": vibration,
    "maintenance_hours": maintenance_hours,
    "load": load,
    "failure": failure,
})
print(f"故障率: {data['failure'].mean():.1%}")


# =============================================================================
# 2. 学習用とテスト用に分ける
# =============================================================================

X = data.drop(columns="failure")
y = data["failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)


# =============================================================================
# 3. 少数派（故障）クラスへ大きな重みを付ける
# =============================================================================

# TODO: 正常件数を故障件数で割った比率positive_weightを求め、
#       故障サンプルにはpositive_weight、正常サンプルには1.0を割り当てた
#       sample_weight配列を作ってください
# ヒント： positive_weight = (y_train == 0).sum() / (y_train == 1).sum()
#         sample_weight = np.where(y_train == 1, positive_weight, 1.0)
positive_weight = None
sample_weight = None


# =============================================================================
# 4. 勾配ブースティングモデルを学習する
# =============================================================================

# TODO: HistGradientBoostingClassifierを作成し、sample_weightを使って学習させてください
# ヒント： HistGradientBoostingClassifier(max_iter=180, learning_rate=0.06,
#                                        max_leaf_nodes=15, random_state=42)
#         model.fit(X_train, y_train, sample_weight=sample_weight)
model = None

prob = model.predict_proba(X_test)[:, 1]


# =============================================================================
# 5. 業務目的に合わせたしきい値で故障を判定する
# =============================================================================

# TODO: 標準の0.5ではなく、しきい値0.35で故障(1)・正常(0)を判定したpredを作ってください
# ヒント： threshold = 0.35
#         pred = (prob >= threshold).astype(int)
threshold = 0.35
pred = None

print(f"ROC-AUC: {roc_auc_score(y_test, prob):.3f}")
print(classification_report(y_test, pred, target_names=["Normal", "Failure"], zero_division=0))

ConfusionMatrixDisplay.from_predictions(
    y_test, pred, display_labels=["Normal", "Failure"], cmap="Oranges"
)
plt.title(f"Failure Detection (threshold={threshold})")
plt.tight_layout()
plt.show()

print("しきい値を下げると見逃しは減りやすい一方、誤警報と点検コストが増えます。")
