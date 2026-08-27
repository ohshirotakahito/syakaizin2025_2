# -*- coding: utf-8 -*-
"""
D1 演習課題7（問題版）：工場設備の故障を予測するモデルを選ぼう
==========================================================

【この課題で行うこと】
あなたは食品工場の予知保全担当者です。センサーデータから、設備が24時間以内に
故障するかを予測します。今回は次の3モデルを交差検証で比較します。

・ロジスティック回帰
・k近傍法（k-NN）
・ランダムフォレスト

予測するfailure_within_24hは「正常=0」「故障=1」の2種類なので分類問題です。
工場では故障の見逃しが停止、廃棄、安全事故につながる可能性があります。その
ため、今回は正解率だけでなく、故障をどれだけ発見できたかを表す再現率を重視します。

【主な用語】
・交差検証：学習データの分け方を変えながら、複数回性能を測る方法
・accuracy：正常と故障を含む、予測全体の正解率
・recall：実際に故障した設備のうち、故障と予測できた割合
・ROC-AUC：故障設備を正常設備より高リスクに順位付けする能力
・Pipeline：標準化とモデルなど、複数の処理を順番につなぐ仕組み

【取り組み方】
コードをすべて一から書く必要はありません。選択肢を読み、「____」だけを
埋めてください。モデル比較表の作成とグラフ描画は完成コードを用意しています。

注意：「____」が残っている間は、プログラムは正しく実行できません。
データは演習用に生成した架空データです。
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


# ==================================================================
# 準備：架空の設備センサーデータを作る
# ==================================================================
# 800件のデータを生成します。乱数の種を42に固定しているため、毎回同じ
# データになります。
rng = np.random.default_rng(42)
n = 800
temperature_c = np.clip(rng.normal(68, 9, n), 35, 105)
vibration_mm_s = np.clip(rng.gamma(2.2, 1.4, n), 0.2, 14)
pressure_kpa = np.clip(rng.normal(205, 25, n), 120, 290)
motor_current_a = np.clip(rng.normal(18, 4, n), 7, 34)
hours_since_maintenance = rng.integers(10, 1500, n)
production_speed = np.clip(rng.normal(92, 15, n), 45, 135)

# 高温、振動、電流、整備後の経過時間などから、架空の故障確率を作ります。
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
print(f"\nデータ件数: {len(machines)}件")
print(f"故障件数: {machines['failure_within_24h'].sum()}件")
print(f"故障率: {machines['failure_within_24h'].mean():.1%}")


# ==================================================================
# 問題1：説明変数Xと目的変数yを分けよう
# ==================================================================
# Xには予測の手掛かりとなる6つのセンサー項目を入れます。予測したい
# failure_within_24hはdrop()で除きます。
#
# 問題1-A：「____」へ入る列名を選んでください。
# 選択肢：A. "failure_within_24h"    B. "temperature_c"
#         C. "production_speed"
# 自分の答え：
X = machines.drop(columns=____)

# 問題1-B：yには予測したい列を指定します。
# 選択肢：A. "vibration_mm_s"    B. "failure_within_24h"
#         C. "pressure_kpa"
# 自分の答え：
y = machines[____]


# ==================================================================
# 問題2：最終評価用のテストデータを確保しよう
# ==================================================================
# 学習用75%、テスト用25%に分けます。stratify=yを指定すると、学習用と
# テスト用の故障率をほぼ同じに保てます。
#
# 選択肢：A. 0.25    B. 0.75    C. 25
# 自分の答え：
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=____,
    random_state=42,
    stratify=y,
)


# 【確認問題1】stratify=yを指定する目的はどれですか。
# A. 学習用とテスト用の故障率をほぼ同じにする
# B. 故障データをすべて削除する
# C. センサー値を標準化する
# 自分の答え：


# ==================================================================
# 問題3：比較する3モデルを準備しよう
# ==================================================================
# ロジスティック回帰とk-NNは、項目の単位や数値の大きさの影響を受けるため、
# StandardScalerとPipelineでつなぎます。ランダムフォレストは木の分岐を使い、
# 距離を直接計算しないため、通常は標準化が不要です。
#
# 問題3-A：ロジスティック回帰のクラス名を選んでください。
# 選択肢：A. LogisticRegression    B. LinearRegression
#         C. KNeighborsClassifier
#
# 問題3-B：k-NNのクラス名を選んでください。
# 選択肢：A. RandomForestClassifier    B. KNeighborsClassifier
#         C. StandardScaler
#
# 問題3-C：ランダムフォレストのクラス名を選んでください。
# 選択肢：A. RandomForestClassifier    B. LogisticRegression
#         C. ConfusionMatrixDisplay
# 自分の答え：
models = {
    "Logistic regression": make_pipeline(
        StandardScaler(),
        ____(max_iter=2000, class_weight="balanced"),
    ),
    "k-NN": make_pipeline(
        StandardScaler(),
        ____(n_neighbors=9, weights="distance"),
    ),
    "Random forest": ____(
        n_estimators=250,
        random_state=42,
        class_weight="balanced",
    ),
}


# 【確認問題2】ランダムフォレストで標準化が通常不要なのはなぜですか。
# A. 特徴量の大小関係で分岐する木を使い、距離を直接計算しないから
# B. データを1列しか使わないから
# C. 目的変数を使わないから
# 自分の答え：


# ==================================================================
# 問題4：5分割交差検証で3モデルを比較しよう
# ==================================================================
# accuracy、recall、ROC-AUCの3指標を比較します。今回は故障の見逃しを
# 重視するため、後でrecallが最大のモデルを選びます。
scoring = ["accuracy", "recall", "roc_auc"]
comparison_rows = []

for name, candidate_model in models.items():
    # cvは、学習データをいくつに分けて交差検証するかを指定します。
    # 選択肢：A. 2    B. 5    C. 800
    # 自分の答え：
    scores = cross_validate(
        candidate_model,
        X_train,
        y_train,
        cv=____,
        scoring=scoring,
    )

    # 各分割で得たスコアの平均を保存します。この処理は記入済みです。
    comparison_rows.append({
        "model": name,
        "accuracy": scores["test_accuracy"].mean(),
        "recall": scores["test_recall"].mean(),
        "roc_auc": scores["test_roc_auc"].mean(),
    })

comparison = pd.DataFrame(comparison_rows).set_index("model")
print("\n【5分割交差検証の平均】")
print(comparison.round(3))


# 【確認問題3】交差検証を使う理由はどれですか。
# A. 1回の分割結果だけに依存せず、安定して性能を比較するため
# B. データ件数を実際に増やすため
# C. 故障した設備を修理するため
# 自分の答え：


# ==================================================================
# 問題5：業務目的に合うモデルを選ぼう
# ==================================================================
# 今回は故障の見逃しを減らしたいため、recallが最大のモデルを選びます。
# idxmax()は、指定した列で最大値を持つ行名を返します。
#
# 選択肢：A. "accuracy"    B. "recall"    C. "roc_auc"
# 自分の答え：
best_model_name = comparison[____].idxmax()
best_model = models[best_model_name]
print(f"\n採用モデル: {best_model_name}（再現率を重視）")


# 【確認問題4】故障クラスのrecallが低いと何が起きますか。
# A. 実際の故障を正常と予測する見逃しが増える
# B. 正常設備がすべて故障する
# C. センサーの数が減る
# 自分の答え：


# ==================================================================
# 問題6：採用モデルを学習し、テストデータで最終評価しよう
# ==================================================================
# 問題6-A：学習用データで学習するメソッドを選んでください。
# 選択肢：A. fit    B. predict    C. round
# 自分の答え：
best_model.____(X_train, y_train)

# 問題6-B：テストデータの故障有無を予測するメソッドを選んでください。
# 選択肢：A. fit    B. predict    C. mean
# 自分の答え：
test_prediction = best_model.____(X_test)

# 問題6-C：故障クラスの再現率を求める関数を選んでください。
# 選択肢：A. recall_score    B. classification_report
#         C. cross_validate
# 自分の答え：
test_recall = ____(y_test, test_prediction)

print(f"テストデータの故障再現率: {test_recall:.3f}")
print(classification_report(
    y_test,
    test_prediction,
    target_names=["Normal", "Failure"],
    zero_division=0,
))


# ==================================================================
# 準備：モデル比較と混同行列をグラフで確認しよう
# ==================================================================
# 描画処理は複雑なので記入済みです。左の棒グラフで3モデルの交差検証結果、
# 右の混同行列で採用モデルの正解・誤りの内訳を確認します。
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
comparison.plot(
    kind="bar",
    ylim=(0, 1),
    ax=axes[0],
    color=["#4C78A8", "#F58518", "#54A24B"],
)
axes[0].set_title("Cross-validation Model Comparison")
axes[0].set_ylabel("Score")
axes[0].tick_params(axis="x", rotation=15)
axes[0].grid(axis="y", alpha=0.25)
axes[0].legend(loc="lower right")

ConfusionMatrixDisplay.from_predictions(
    y_test,
    test_prediction,
    display_labels=["Normal", "Failure"],
    cmap="Oranges",
    ax=axes[1],
)
axes[1].set_title(f"Selected Model: {best_model_name}")
fig.tight_layout()
plt.show()


# ==================================================================
# 最後の考察
# ==================================================================
# 1. 故障の見逃しと誤警報では、どちらの影響が大きいでしょうか。
#    工場停止、安全事故、不要な点検の費用を考えて答えてください。
# 自分の答え：


# 2. 予測に追加したい情報を2つ以上選んでください。
# A. 異音センサー    B. 潤滑油の状態    C. 過去の部品交換履歴
# D. 設備番号の桁数  E. ファイルの保存時刻
# 自分の答え：


# 3. モデルが故障と予測しただけで、設備を即時停止してよいでしょうか。
#    センサーの再確認、現場担当者の点検、生産への影響など、必要な確認手順を
#    考えてください。
# 自分の答え：


print("【実務上の判断】")
print("故障の見逃しは停止・廃棄・安全事故につながるため、正解率だけでなく")
print("故障クラスの再現率を重視します。一方、誤警報による点検コストとの")
print("バランスも、運用開始前に現場と決める必要があります。")
