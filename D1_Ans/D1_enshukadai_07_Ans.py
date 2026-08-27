# -*- coding: utf-8 -*-
"""
D1 演習課題7（解答版）：工場設備の故障を予測するモデルを選ぼう
==========================================================

あなたは食品工場の予知保全担当者です。センサーデータから24時間以内の
設備故障を予測し、ロジスティック回帰、k-NN、ランダムフォレストを
交差検証で比較します。データは演習用の架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, recall_score
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# 再現可能な架空センサーデータを800件生成します。
rng = np.random.default_rng(42)
n = 800
temperature_c = np.clip(rng.normal(68, 9, n), 35, 105)
vibration_mm_s = np.clip(rng.gamma(2.2, 1.4, n), 0.2, 14)
pressure_kpa = np.clip(rng.normal(205, 25, n), 120, 290)
motor_current_a = np.clip(rng.normal(18, 4, n), 7, 34)
hours_since_maintenance = rng.integers(10, 1500, n)
production_speed = np.clip(rng.normal(92, 15, n), 45, 135)

# 高温・振動・電流・整備後時間などから故障確率を生成します。
failure_score = (
    -4.0
    + 0.055 * (temperature_c - 65)
    + 0.42 * (vibration_mm_s - 3)
    + 0.045 * (motor_current_a - 18)
    + 0.0018 * (hours_since_maintenance - 600)
    + 0.018 * (production_speed - 90)
    + 0.0007 * (pressure_kpa - 205) ** 2
)
failure_probability = 1 / (1 + np.exp(-failure_score))
failure_within_24h = rng.binomial(1, failure_probability)

machines = pd.DataFrame({
    "temperature_c": temperature_c.round(1),
    "vibration_mm_s": vibration_mm_s.round(2),
    "pressure_kpa": pressure_kpa.round(1),
    "motor_current_a": motor_current_a.round(1),
    "hours_since_maintenance": hours_since_maintenance,
    "production_speed": production_speed.round(1),
    "failure_within_24h": failure_within_24h,
})

print("【設備データ】")
print(machines.head())
print(f"\n故障率: {machines['failure_within_24h'].mean():.1%}")


# 説明変数Xと目的変数yを分け、最終評価用のテストデータを確保します。
X = machines.drop(columns="failure_within_24h")
y = machines["failure_within_24h"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)


# 距離や係数を使う2モデルは標準化とPipelineでつなぎます。
# 木構造を使うランダムフォレストは、通常は標準化が不要です。
models = {
    "Logistic regression": make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced")
    ),
    "k-NN": make_pipeline(
        StandardScaler(), KNeighborsClassifier(n_neighbors=9, weights="distance")
    ),
    "Random forest": RandomForestClassifier(
        n_estimators=250, random_state=42, class_weight="balanced"
    ),
}


# 故障の見逃しを重視するためrecallを中心に、accuracyとROC-AUCも評価します。
scoring = ["accuracy", "recall", "roc_auc"]
comparison_rows = []

for name, candidate_model in models.items():
    # 学習データ内で5分割交差検証を行います。
    scores = cross_validate(candidate_model, X_train, y_train, cv=5, scoring=scoring)
    comparison_rows.append({
        "model": name,
        "accuracy": scores["test_accuracy"].mean(),
        "recall": scores["test_recall"].mean(),
        "roc_auc": scores["test_roc_auc"].mean(),
    })

comparison = pd.DataFrame(comparison_rows).set_index("model")
print("\n【5分割交差検証の平均】")
print(comparison.round(3))


# 今回は故障の見逃しを減らす目的なので、recall最大のモデルを選びます。
best_model_name = comparison["recall"].idxmax()
best_model = models[best_model_name]
print(f"\n採用モデル: {best_model_name}（再現率を重視）")


# 採用モデルを全学習データで学習し、未使用のテストデータで最終評価します。
best_model.fit(X_train, y_train)
test_prediction = best_model.predict(X_test)
test_recall = recall_score(y_test, test_prediction)
print(f"テストデータの故障再現率: {test_recall:.3f}")
print(classification_report(
    y_test, test_prediction, target_names=["Normal", "Failure"], zero_division=0
))


# 左にモデル比較、右に採用モデルの混同行列を表示します。
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
comparison.plot(kind="bar", ylim=(0, 1), ax=axes[0],
                color=["#4C78A8", "#F58518", "#54A24B"])
axes[0].set_title("Cross-validation Model Comparison")
axes[0].set_ylabel("Score")
axes[0].tick_params(axis="x", rotation=15)
axes[0].grid(axis="y", alpha=0.25)
axes[0].legend(loc="lower right")

ConfusionMatrixDisplay.from_predictions(
    y_test, test_prediction, display_labels=["Normal", "Failure"],
    cmap="Oranges", ax=axes[1]
)
axes[1].set_title(f"Selected Model: {best_model_name}")
fig.tight_layout()
plt.show()


print("【実務上の判断】")
print("故障の見逃しは停止・廃棄・安全事故につながるため、正解率だけでなく")
print("故障クラスの再現率を重視します。一方、誤警報による点検コストとの")
print("バランスも、運用開始前に現場と決める必要があります。")

