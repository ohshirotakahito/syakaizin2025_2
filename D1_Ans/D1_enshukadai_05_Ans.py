# -*- coding: utf-8 -*-
"""
D1 演習課題5（解答版）：サブスク顧客の解約を予測しよう
====================================================

【設定】
あなたは動画配信サービスのカスタマーサクセス担当者です。解約しそうな顧客へ
早めにサポートを行うため、翌月の解約有無を予測するモデルを作成します。

この演習ではロジスティック回帰を使用し、予測精度だけでなく「解約者の
見逃し」と「継続者への誤った警告」も確認します。

注意：このデータは演習用に生成した架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# random_stateを固定し、実行するたびに同じ架空データを作ります。
rng = np.random.default_rng(42)
number_of_customers = 500


# 顧客の利用状況を、現実的な範囲で生成します。
tenure_months = rng.integers(1, 73, number_of_customers)
monthly_fee_yen = np.clip(rng.normal(7200, 1800, number_of_customers), 2500, 13000)
support_tickets = np.clip(rng.poisson(1.8, number_of_customers), 0, 9)
weekly_hours = np.clip(rng.normal(8.5, 4.0, number_of_customers), 0.2, 25)
payment_delays = np.clip(rng.poisson(0.7, number_of_customers), 0, 6)
contract_months = rng.choice([1, 12, 24], number_of_customers, p=[0.45, 0.35, 0.20])


# 解約しやすさを表す架空のスコアを作ります。
# 長期利用・長期契約・利用時間の多さは解約を抑える方向、料金・問い合わせ・
# 支払い遅延は解約を増やす方向に設定しています。
churn_score = (
    0.3
    - 0.025 * tenure_months
    + 0.00022 * (monthly_fee_yen - 7000)
    + 0.28 * support_tickets
    - 0.055 * weekly_hours
    + 0.45 * payment_delays
    - 0.055 * contract_months
)


# ロジスティック関数でスコアを0から1の解約確率へ変換します。
churn_probability = 1 / (1 + np.exp(-churn_score))

# 各顧客について乱数と確率を比較し、翌月解約を0または1で生成します。
churn_next_month = rng.binomial(1, churn_probability)


# 分析しやすいよう、すべての項目をDataFrameにまとめます。
customers = pd.DataFrame({
    "tenure_months": tenure_months,
    "monthly_fee_yen": monthly_fee_yen.round().astype(int),
    "support_tickets": support_tickets,
    "weekly_hours": weekly_hours.round(1),
    "payment_delays": payment_delays,
    "contract_months": contract_months,
    "churn_next_month": churn_next_month,
})

print("【顧客データ：先頭5行】")
print(customers.head())
print(f"\n顧客数: {len(customers)}人")
print(f"解約者数: {customers['churn_next_month'].sum()}人")
print(f"解約率: {customers['churn_next_month'].mean():.1%}")


# Xは予測に使う説明変数、yは予測したい目的変数です。
X = customers.drop(columns="churn_next_month")
y = customers["churn_next_month"]


# 学習用75%、テスト用25%に分けます。
# stratify=yにより、学習用とテスト用の解約率をほぼ同じに保ちます。
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)


# 標準化とロジスティック回帰をPipelineで一つにつなぎます。
# Pipelineにすると、テストデータへ学習用データの基準で標準化を適用でき、
# テストデータの情報が学習へ漏れる「データリーク」を防げます。
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=2000),
)

# 学習用データから、解約と各特徴量の関係を学習します。
model.fit(X_train, y_train)


# predict()は0または1、predict_proba()は解約確率を返します。
predicted_class = model.predict(X_test)
predicted_probability = model.predict_proba(X_test)[:, 1]


# 正解率は全予測のうち正しかった割合です。
accuracy = accuracy_score(y_test, predicted_class)

# ROC-AUCは、解約者を継続者より高リスクと順位付けできる能力を表します。
# 0.5はランダムに近く、1.0に近いほど識別能力が高いことを示します。
auc = roc_auc_score(y_test, predicted_probability)

print("\n【モデル評価】")
print(f"正解率: {accuracy:.3f}")
print(f"ROC-AUC: {auc:.3f}")
print("\n【分類レポート】")
print(classification_report(
    y_test, predicted_class,
    target_names=["継続", "解約"],
    zero_division=0,
))


# 混同行列から、4種類の予測結果を取り出します。
tn, fp, fn, tp = confusion_matrix(y_test, predicted_class).ravel()
print("【混同行列の読み取り】")
print(f"継続を正しく予測: {tn}人")
print(f"継続者を解約と誤予測: {fp}人")
print(f"解約者を見逃し: {fn}人")
print(f"解約を正しく予測: {tp}人")


# Pipeline内のロジスティック回帰モデルを取り出します。
logistic_model = model.named_steps["logisticregression"]

# 標準化後の係数なので、絶対値で特徴量同士の影響を比較できます。
# 正の係数は解約確率を上げる方向、負の係数は下げる方向です。
coefficients = pd.Series(logistic_model.coef_[0], index=X.columns)
coefficient_table = pd.DataFrame({
    "coefficient": coefficients,
    "absolute_importance": coefficients.abs(),
}).sort_values("absolute_importance", ascending=False)

print("\n【解約予測へ影響した特徴量】")
print(coefficient_table.round(3))


# 混同行列とROC曲線を横に並べます。
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    predicted_class,
    display_labels=["Continue", "Churn"],
    cmap="Blues",
    ax=axes[0],
)
axes[0].set_title("Churn Prediction: Confusion Matrix")

RocCurveDisplay.from_predictions(
    y_test,
    predicted_probability,
    name=f"Logistic regression (AUC={auc:.3f})",
    ax=axes[1],
)
axes[1].plot([0, 1], [0, 1], "--", color="gray", label="Random")
axes[1].set_title("ROC Curve")
axes[1].grid(alpha=0.25)
axes[1].legend()

fig.tight_layout()
plt.show()


# 解約確率が高い順に、テストデータの要フォロー顧客を表示します。
follow_up = X_test.copy()
follow_up["actual_churn"] = y_test
follow_up["predicted_probability"] = predicted_probability
follow_up = follow_up.sort_values("predicted_probability", ascending=False)

print("\n【優先フォロー候補：上位10人】")
print(follow_up.head(10).round(3))

print("\n【実務上の注意】")
print("予測確率は解約の確定ではありません。顧客への不利益な判断には使わず、")
print("サポート案内や満足度確認など、顧客体験を改善する目的で利用します。")

