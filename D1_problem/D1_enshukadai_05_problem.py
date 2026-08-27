# -*- coding: utf-8 -*-
"""
D1 演習課題5（問題版）：サブスク顧客の解約を予測しよう
====================================================

【この課題で行うこと】
あなたは動画配信サービスのカスタマーサクセス担当者です。翌月に解約する
可能性が高い顧客を予測し、早めのサポートにつなげます。

今回は「継続=0」「解約=1」という2種類を予測するため、分類問題です。
ロジスティック回帰を使い、正解率だけでなく、解約者の見逃しや継続者への
誤った警告も確認します。

【主な列】
・tenure_months    ：これまでの利用月数
・monthly_fee_yen  ：月額料金（円）
・support_tickets  ：問い合わせ回数
・weekly_hours     ：1週間あたりの利用時間
・payment_delays   ：支払い遅延回数
・contract_months  ：契約期間（月）
・churn_next_month ：翌月の解約有無（継続=0、解約=1）

【用語】
・説明変数X：予測の手掛かりとして使う列
・目的変数y：モデルが予測する列
・学習データ：モデルが関係を学ぶためのデータ
・テストデータ：未知の顧客に対する性能を確認するためのデータ
・データリーク：本来学習時に使えないテストデータの情報が混ざること

【取り組み方】
すべてを一から書く必要はありません。選択肢を読み、コードの「____」だけを
埋めてください。混同行列の詳しい集計、係数表、グラフなどの複雑な処理は
記入済みです。

注意：「____」が残っている間は、プログラムは正しく実行できません。
このデータは演習用に生成した架空データです。
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


# ==================================================================
# 準備：架空の顧客データを作る
# ==================================================================
# この部分は完成済みです。random_stateに相当する値42を固定しているため、
# 実行するたびに同じ架空データが作られます。
rng = np.random.default_rng(42)
number_of_customers = 500

tenure_months = rng.integers(1, 73, number_of_customers)
monthly_fee_yen = np.clip(
    rng.normal(7200, 1800, number_of_customers), 2500, 13000
)
support_tickets = np.clip(rng.poisson(1.8, number_of_customers), 0, 9)
weekly_hours = np.clip(rng.normal(8.5, 4.0, number_of_customers), 0.2, 25)
payment_delays = np.clip(rng.poisson(0.7, number_of_customers), 0, 6)
contract_months = rng.choice(
    [1, 12, 24], number_of_customers, p=[0.45, 0.35, 0.20]
)

# 架空の解約しやすさを計算します。長期利用、長期契約、利用時間の多さは
# 解約を抑える方向、料金、問い合わせ、支払い遅延は解約を増やす方向です。
churn_score = (
    0.3
    - 0.025 * tenure_months
    + 0.00022 * (monthly_fee_yen - 7000)
    + 0.28 * support_tickets
    - 0.055 * weekly_hours
    + 0.45 * payment_delays
    - 0.055 * contract_months
)
churn_probability = 1 / (1 + np.exp(-churn_score))
churn_next_month = rng.binomial(1, churn_probability)

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


# ==================================================================
# 問題1：説明変数Xと目的変数yを分けよう
# ==================================================================
# Xには予測の手掛かりとなる6列を入れます。予測したいchurn_next_monthを
# Xに含めると答えを事前に教えることになるため、drop()で除きます。
#
# 問題1-A：「____」へ入る列名を選んでください。
# 選択肢：A. "churn_next_month"    B. "monthly_fee_yen"
#         C. "tenure_months"
# 自分の答え：
X = customers.drop(columns=____)

# 問題1-B：yには予測したい列を指定します。
# 選択肢：A. "weekly_hours"    B. "churn_next_month"
#         C. "contract_months"
# 自分の答え：
y = customers[____]


# 【確認問題1】今回の目的変数はどれですか。
# A. monthly_fee_yen    B. churn_next_month    C. tenure_months
# 自分の答え：


# 【確認問題2】今回の問題が「分類」である理由はどれですか。
# A. 解約・継続というカテゴリを予測するから
# B. 月額料金の平均を求めるから
# C. 顧客を料金順に並べるから
# 自分の答え：


# ==================================================================
# 問題2：学習用とテスト用に分けよう
# ==================================================================
# 全データで学習して同じデータで評価すると、未知の顧客への性能が分かりません。
# そこで75%を学習用、25%をテスト用に分けます。
#
# test_sizeはテスト用データの割合です。
# 選択肢：A. 0.25    B. 0.75    C. 25
# 自分の答え：
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=____,
    random_state=42,
    stratify=y,
)


# stratify=yは、学習用とテスト用で解約率が大きく変わらないようにします。
# 【確認問題3】テストデータを分ける主な理由はどれですか。
# A. 未知の顧客に対する予測性能を確かめるため
# B. 説明変数の列数を増やすため
# C. 解約者をすべて削除するため
# 自分の答え：


# ==================================================================
# 問題3：標準化とロジスティック回帰をつなごう
# ==================================================================
# Pipelineを使うと、学習用データで求めた標準化の基準を、テストデータにも
# 安全に適用できます。テストデータの情報が学習へ混ざることも防げます。
#
# 問題3-A：最初に入れる標準化処理を選んでください。
# 選択肢：A. StandardScaler()    B. accuracy_score()
#         C. confusion_matrix()
# 自分の答え：
#
# 問題3-B：次に入れる分類モデルを選んでください。
# 選択肢：A. LogisticRegression(max_iter=2000)
#         B. StandardScaler()    C. RocCurveDisplay()
# 自分の答え：
model = make_pipeline(
    ____,
    ____,
)


# ==================================================================
# 問題4：モデルを学習し、テストデータを予測しよう
# ==================================================================
# fit()は学習用データから関係を学ぶメソッドです。
# 選択肢：A. fit    B. predict    C. round
# 自分の答え：
model.____(X_train, y_train)


# predict()は0または1の予測クラスを返します。
# 選択肢：A. predict    B. predict_proba    C. fit
# 自分の答え：
predicted_class = model.____(X_test)


# predict_proba()は各クラスの予測確率を返します。[:, 1]で、2列目にある
# 「解約=1」の確率だけを取り出します。
# 選択肢：A. fit    B. predict    C. predict_proba
# 自分の答え：
predicted_probability = model.____(X_test)[:, 1]


# 【確認問題4】Pipelineを使う利点として正しいものはどれですか。
# A. 学習と予測で同じ前処理を安全に適用できる
# B. 正解率を必ず100%にできる
# C. テストデータを使って標準化の基準を学習できる
# 自分の答え：


# ==================================================================
# 問題5：正解率とROC-AUCを計算しよう
# ==================================================================
# 正解率は、全予測のうち正しかった割合です。
# 選択肢：A. accuracy_score    B. roc_auc_score
#         C. classification_report
# 自分の答え：
accuracy = ____(y_test, predicted_class)

# ROC-AUCは、解約者を継続者より高リスクに順位付けできる能力を表します。
# 0.5に近いとランダム、1.0に近いほど識別能力が高いと解釈します。
# 選択肢：A. accuracy_score    B. roc_auc_score
#         C. confusion_matrix
# 自分の答え：
auc = ____(y_test, predicted_probability)

print("\n【モデル評価】")
print(f"正解率: {accuracy:.3f}")
print(f"ROC-AUC: {auc:.3f}")
print("\n【分類レポート】")
print(classification_report(
    y_test,
    predicted_class,
    target_names=["継続", "解約"],
    zero_division=0,
))


# ==================================================================
# 準備：混同行列を4種類に分けて確認しよう
# ==================================================================
# この処理は記入済みです。実際の値と予測値を組み合わせ、次の4種類を数えます。
# TN：継続者を正しく継続と予測
# FP：継続者を誤って解約と予測
# FN：解約者を誤って継続と予測（解約者の見逃し）
# TP：解約者を正しく解約と予測
tn, fp, fn, tp = confusion_matrix(y_test, predicted_class).ravel()
print("【混同行列の読み取り】")
print(f"継続を正しく予測: {tn}人")
print(f"継続者を解約と誤予測: {fp}人")
print(f"解約者を見逃し: {fn}人")
print(f"解約を正しく予測: {tp}人")


# 【確認問題5】「実際は解約したが、継続と予測した」ケースはどれですか。
# A. TN    B. FP    C. FN    D. TP
# 自分の答え：


# 【確認問題6】解約防止のため、特に減らしたい見逃しはどれですか。
# A. FP    B. FN
# 自分の答え：
# 理由：


# ==================================================================
# 準備：解約予測へ影響した特徴量を確認しよう
# ==================================================================
# Pipeline内のロジスティック回帰を取り出し、係数を表にします。
# 標準化後なので、係数の絶対値で特徴量同士の影響の強さを比較できます。
# 正の係数は解約確率を上げる方向、負の係数は下げる方向です。
logistic_model = model.named_steps["logisticregression"]
coefficients = pd.Series(logistic_model.coef_[0], index=X.columns)
coefficient_table = pd.DataFrame({
    "coefficient": coefficients,
    "absolute_importance": coefficients.abs(),
}).sort_values("absolute_importance", ascending=False)

print("\n【解約予測へ影響した特徴量】")
print(coefficient_table.round(3))


# 【確認問題7】係数が大きな正の値である場合、正しい説明はどれですか。
# A. その特徴量が増えるほど、解約確率が高くなる方向に関係する
# B. その特徴量はモデルから削除された
# C. その特徴量の値は必ず1になる
# 自分の答え：


# ==================================================================
# 準備：混同行列とROC曲線を表示しよう
# ==================================================================
# 描画コードは複雑なので記入済みです。左で4種類の予測数、右でモデルが
# 解約者と継続者を順位付けする性能を確認します。
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


# ==================================================================
# 準備：優先フォロー候補を表示しよう
# ==================================================================
# テストデータへ実際の解約有無と予測確率を追加し、予測確率が高い順に
# 並べます。この順位はフォローを検討する手掛かりであり、解約の確定では
# ありません。
follow_up = X_test.copy()
follow_up["actual_churn"] = y_test
follow_up["predicted_probability"] = predicted_probability
follow_up = follow_up.sort_values("predicted_probability", ascending=False)

print("\n【優先フォロー候補：上位10人】")
print(follow_up.head(10).round(3))


# ==================================================================
# 最後の考察
# ==================================================================
# 1. 解約確率が高い顧客へ、どのような支援を提案しますか。
# A. 満足度の確認や利用方法の案内
# B. 理由を確認せずサービスを停止
# C. 予測結果を公開
# 自分の答え：
# 具体的な支援案：


# 2. 解約確率が高いという理由だけで、サービス制限や料金変更などの不利益を
# 与えてはいけないのはなぜですか。予測の誤りと顧客への公平性を考えてください。
# 自分の答え：


# 3. よりよい予測のために追加したい情報を2つ以上選んでください。
# A. 視聴ジャンル    B. 最近の利用頻度の変化    C. アンケート満足度
# D. 顧客番号の桁数    E. ファイルを保存した時刻
# 自分の答え：


print("\n【実務上の注意】")
print("予測確率は解約の確定ではありません。顧客への不利益な判断には使わず、")
print("サポート案内や満足度確認など、顧客体験を改善する目的で利用します。")
