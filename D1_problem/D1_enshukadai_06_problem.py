# -*- coding: utf-8 -*-
"""
D1 演習課題6（問題版）：フードデリバリーの所要時間を予測しよう
==========================================================

【この課題で行うこと】
あなたはフードデリバリー会社のデータ分析担当者です。注文時に分かる情報から、
配達完了までに何分かかるかを予測し、お客様へ到着予定時間を案内します。

予測するdelivery_minutesは、分単位の連続した数値です。そのため、これは
「分類」ではなく「回帰」の問題です。今回は線形回帰を使用します。

【予測に使う項目】
・distance_km             ：配達距離（km）
・item_count              ：商品の個数
・restaurant_prep_minutes ：店舗の調理予定時間（分）
・traffic_level           ：交通量（1=少、2=中、3=多）
・is_raining              ：雨かどうか（0=晴れ、1=雨）
・courier_active_orders   ：配達員が担当中の注文数

【用語】
・説明変数X：予測の手掛かりとして使う6項目
・目的変数y：予測したい配達時間
・MAE：予測が実際の時間から平均で何分ずれたか
・RMSE：大きな予測誤差をMAEより強く評価する指標
・R²：配達時間のばらつきをモデルがどの程度説明できたか
・残差：実際の時間から予測時間を引いた値

【取り組み方】
選択肢を読み、コード中の「____」だけを埋めてください。係数表、結果表、
グラフ描画などの複雑な処理は記入済みです。

注意：「____」が残っている間は、プログラムは正しく実行できません。
このデータは演習用に生成した架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# ==================================================================
# 準備：架空の配達データを作る
# ==================================================================
# この部分は完成済みです。乱数の種を42に固定しているため、毎回同じデータを
# 作ることができます。
rng = np.random.default_rng(42)
number_of_orders = 600

distance_km = rng.uniform(0.5, 12.0, number_of_orders)
item_count = rng.integers(1, 9, number_of_orders)
restaurant_prep_minutes = np.clip(
    rng.normal(16, 5, number_of_orders), 5, 35
)
traffic_level = rng.integers(1, 4, number_of_orders)
is_raining = rng.binomial(1, 0.25, number_of_orders)
courier_active_orders = rng.integers(1, 5, number_of_orders)

# 現実には同じ条件でも時間が完全には一致しないため、予測しきれない揺らぎを
# noiseとして加えています。
noise = rng.normal(0, 4.5, number_of_orders)
delivery_minutes = (
    5
    + 3.2 * distance_km
    + 0.9 * item_count
    + 0.75 * restaurant_prep_minutes
    + 4.5 * (traffic_level - 1)
    + 6.0 * is_raining
    + 2.8 * (courier_active_orders - 1)
    + noise
)

deliveries = pd.DataFrame({
    "distance_km": distance_km.round(2),
    "item_count": item_count,
    "restaurant_prep_minutes": restaurant_prep_minutes.round(1),
    "traffic_level": traffic_level,
    "is_raining": is_raining,
    "courier_active_orders": courier_active_orders,
    "delivery_minutes": delivery_minutes.round(1),
})

print("【配達データ：先頭5行】")
print(deliveries.head())
print(f"\n注文数: {len(deliveries)}件")
print(f"平均配達時間: {deliveries['delivery_minutes'].mean():.1f}分")


# ==================================================================
# 問題1：説明変数Xと目的変数yを分けよう
# ==================================================================
# Xには予測の手掛かりとなる6列を入れます。予測したいdelivery_minutesは
# drop()で除きます。
#
# 問題1-A：「____」へ入る列名を選んでください。
# 選択肢：A. "delivery_minutes"    B. "distance_km"
#         C. "traffic_level"
# 自分の答え：
X = deliveries.drop(columns=____)

# 問題1-B：yには予測したい列を指定します。
# 選択肢：A. "item_count"    B. "delivery_minutes"
#         C. "is_raining"
# 自分の答え：
y = deliveries[____]


# 【確認問題1】今回の分析が回帰である理由はどれですか。
# A. 配達する・しないの2種類を予測するから
# B. 配達時間という連続した数値を予測するから
# C. 注文をいくつかのグループへ分けるから
# 自分の答え：


# ==================================================================
# 問題2：学習用とテスト用に分けよう
# ==================================================================
# 75%を学習用、25%をテスト用に分けます。テストデータはモデルの学習に
# 使用せず、未知の注文に対する予測性能の確認に使います。
#
# 選択肢：A. 0.25    B. 0.75    C. 25
# 自分の答え：
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=____,
    random_state=42,
)


# 【確認問題2】分類で使ったstratifyを今回は指定しない主な理由はどれですか。
# A. 目的変数が連続値であり、分類クラスではないから
# B. テストデータが不要だから
# C. 説明変数が6個あるから
# 自分の答え：


# ==================================================================
# 問題3：線形回帰モデルを学習しよう
# ==================================================================
# 問題3-A：「____」へ入るモデル名を選んでください。
# 選択肢：A. LinearRegression    B. train_test_split
#         C. mean_absolute_error
# 自分の答え：
model = ____()

# 問題3-B：学習用データから関係を学ぶメソッドを選んでください。
# 選択肢：A. fit    B. predict    C. round
# 自分の答え：
model.____(X_train, y_train)

# 問題3-C：テストデータの配達時間を予測するメソッドを選んでください。
# 選択肢：A. fit    B. predict    C. drop
# 自分の答え：
predicted = model.____(X_test)


# ==================================================================
# 問題4：予測性能を3つの指標で評価しよう
# ==================================================================
# 問題4-A：MAEを求める関数を選んでください。
# 選択肢：A. mean_absolute_error    B. mean_squared_error
#         C. r2_score
# 自分の答え：
mae = ____(y_test, predicted)

# 問題4-B：RMSEは、平均二乗誤差の平方根です。
# 1つ目：A. np.sqrt    B. np.mean    C. np.round
# 2つ目：A. mean_absolute_error    B. mean_squared_error
#        C. r2_score
# 自分の答え：
rmse = ____(____(y_test, predicted))

# 問題4-C：決定係数R²を求める関数を選んでください。
# 選択肢：A. r2_score    B. mean_absolute_error
#         C. train_test_split
# 自分の答え：
r2 = ____(y_test, predicted)

print("\n【モデル評価】")
print(f"平均絶対誤差（MAE）: {mae:.2f}分")
print(f"二乗平均平方根誤差（RMSE）: {rmse:.2f}分")
print(f"決定係数（R2）: {r2:.3f}")


# 【確認問題3】MAEが4.0分だった場合の正しい説明はどれですか。
# A. すべての予測が必ず4分遅い
# B. 予測は実際の時間から平均して約4分ずれている
# C. 4%の注文だけ正しく予測できた
# 自分の答え：


# 【確認問題4】R²が1に近い場合の正しい説明はどれですか。
# A. モデルが配達時間のばらつきをよく説明できている
# B. すべての係数が1である
# C. 予測誤差が必ず1分である
# 自分の答え：


# ==================================================================
# 準備：各項目の回帰係数を確認しよう
# ==================================================================
# この表を作るコードは記入済みです。係数は、ほかの条件が同じとき、その項目が
# 1増えることで予測時間が何分変わるかを表します。
coefficient_table = pd.DataFrame({
    "feature": X.columns,
    "coefficient_minutes": model.coef_,
}).sort_values("coefficient_minutes", ascending=False)

print("\n【各項目の回帰係数】")
print(coefficient_table.round(3).to_string(index=False))
print(f"切片: {model.intercept_:.3f}分")


# 【確認問題5】distance_kmの係数が約3.2の場合、正しい説明はどれですか。
# A. ほかの条件が同じなら、距離が1km増えると予測時間が約3.2分長くなる
# B. すべての配達距離が3.2kmである
# C. 配達時間を必ず3.2分以内にできる
# 自分の答え：


# ==================================================================
# 準備：テストデータの予測結果を表にしよう
# ==================================================================
results = X_test.copy()
results["actual_minutes"] = y_test
results["predicted_minutes"] = predicted
results["error_minutes"] = predicted - y_test

print("\n【予測結果：先頭10件】")
print(results.head(10).round(1))


# ==================================================================
# 問題5：新しい注文の配達時間を予測しよう
# ==================================================================
# 新しい注文は次の条件です。DataFrameを作る処理は記入済みです。
# 距離5.5km、商品3点、調理18分、交通量3、雨あり、担当注文2件
new_order = pd.DataFrame({
    "distance_km": [5.5],
    "item_count": [3],
    "restaurant_prep_minutes": [18.0],
    "traffic_level": [3],
    "is_raining": [1],
    "courier_active_orders": [2],
})

# 学習済みモデルで新しい注文を予測します。predict()の結果は配列なので、
# [0]で最初の予測値を取り出します。
# 選択肢：A. fit    B. predict    C. mean
# 自分の答え：
new_prediction = model.____(new_order)[0]

print("\n【新しい注文の予測】")
print(new_order)
print(f"予想到着時間: 注文から約{new_prediction:.0f}分後")
print(f"通常の誤差幅を考慮した案内例: 約{new_prediction - mae:.0f}〜"
      f"{new_prediction + mae:.0f}分後")


# 【確認問題6】お客様への案内として適切なのはどれですか。
# A. 予測値を確定時刻として断言する
# B. 通常の誤差を考慮し、幅を持った到着予定として案内する
# C. 予測結果を案内せず、必ず最短時間だけを表示する
# 自分の答え：


# ==================================================================
# 準備：実測値・予測値・残差をグラフで確認しよう
# ==================================================================
# 描画コードは複雑なので記入済みです。左は実測値と予測値の比較、右は
# 予測値と残差の関係です。点が左の対角線に近いほど予測誤差が小さく、
# 右の残差が0付近へ規則性なく散らばるほど、線形回帰の当てはまりは良好です。
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(y_test, predicted, alpha=0.7, color="#4C78A8")
value_min = min(y_test.min(), predicted.min())
value_max = max(y_test.max(), predicted.max())
axes[0].plot([value_min, value_max], [value_min, value_max],
             "--", color="#E45756", label="Perfect prediction")
axes[0].set_xlabel("Actual delivery time (minutes)")
axes[0].set_ylabel("Predicted delivery time (minutes)")
axes[0].set_title("Actual vs Predicted")
axes[0].grid(alpha=0.25)
axes[0].legend()

residuals = y_test - predicted
axes[1].scatter(predicted, residuals, alpha=0.7, color="#54A24B")
axes[1].axhline(0, color="#E45756", linestyle="--")
axes[1].set_xlabel("Predicted delivery time (minutes)")
axes[1].set_ylabel("Residual: actual - predicted (minutes)")
axes[1].set_title("Residual Plot")
axes[1].grid(alpha=0.25)
fig.tight_layout()
plt.show()


# 【確認問題7】良い残差プロットの特徴はどれですか。
# A. 残差が0付近へ、はっきりした規則性なく散らばっている
# B. すべての残差が右肩上がりに並ぶ
# C. 残差がすべて正になる
# 自分の答え：


# ==================================================================
# 最後の考察
# ==================================================================
# 1. 今回のデータにない要因で、配達時間に影響しそうなものを2つ以上
# 選んでください。
# A. 店舗の実際の混雑    B. 事故や通行止め    C. 住所確認の難しさ
# D. 注文番号の桁数      E. ファイルの保存時刻
# 自分の答え：


# 2. 予測より実際の配達が遅れた注文を、どのように業務改善へ活用できますか。
# 自分の答え：


# 3. 雨が非常に強い場合だけ急に配達時間が増えるなど、単純な直線では
# 表しにくい関係があるとき、今回の線形回帰にはどのような限界がありますか。
# 自分の答え：


print("\n【実務上の注意】")
print("予測値は確定時刻ではありません。交通事故、店舗混雑、住所確認など、")
print("データにない要因でも遅れるため、幅を持たせて案内することが重要です。")
