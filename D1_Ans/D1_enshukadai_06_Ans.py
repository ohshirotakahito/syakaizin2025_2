# -*- coding: utf-8 -*-
"""
D1 演習課題6（解答版）：フードデリバリーの所要時間を予測しよう
==========================================================

【設定】
あなたはフードデリバリー会社のデータ分析担当者です。注文時に表示する
「到着予定時間」を改善するため、注文・天候・交通状況から配達完了までの
所要時間を予測します。

目的変数が分単位の連続した数値なので、これは回帰問題です。
演習用に生成した架空データを使用します。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# 乱数を固定し、実行するたびに同じデータを生成します。
rng = np.random.default_rng(42)
number_of_orders = 600


# 注文時点で分かる情報を現実的な範囲で生成します。
distance_km = rng.uniform(0.5, 12.0, number_of_orders)
item_count = rng.integers(1, 9, number_of_orders)
restaurant_prep_minutes = np.clip(rng.normal(16, 5, number_of_orders), 5, 35)
traffic_level = rng.integers(1, 4, number_of_orders)  # 1=少、2=中、3=多
is_raining = rng.binomial(1, 0.25, number_of_orders)  # 0=晴れ、1=雨
courier_active_orders = rng.integers(1, 5, number_of_orders)


# 所要時間を作ります。各要因の影響に加え、現実の予測しきれない揺らぎを
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


# 説明変数と目的変数を1つのDataFrameへまとめます。
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


# Xは予測に使う説明変数、yは予測したい配達時間です。
X = deliveries.drop(columns="delivery_minutes")
y = deliveries["delivery_minutes"]


# 学習用75%、テスト用25%に分割します。
# 回帰では目的変数が連続値なので、分類で使ったstratifyは指定しません。
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)


# 線形回帰モデルを作り、学習用データから関係を学習します。
model = LinearRegression()
model.fit(X_train, y_train)


# 未使用だったテストデータの配達時間を予測します。
predicted = model.predict(X_test)


# MAEは、予測が実際の値から平均何分ずれたかを表します。
mae = mean_absolute_error(y_test, predicted)

# RMSEは大きな予測誤差をMAEより強く評価します。
rmse = np.sqrt(mean_squared_error(y_test, predicted))

# R2は、配達時間のばらつきをモデルがどの程度説明できたかを表します。
# 1に近いほどよく説明でき、0なら平均値予測と同程度です。
r2 = r2_score(y_test, predicted)

print("\n【モデル評価】")
print(f"平均絶対誤差（MAE）: {mae:.2f}分")
print(f"二乗平均平方根誤差（RMSE）: {rmse:.2f}分")
print(f"決定係数（R2）: {r2:.3f}")


# 係数は、ほかの条件が同じとき、その項目が1増えることで予測時間が
# 何分変化するかを表します。
coefficient_table = pd.DataFrame({
    "feature": X.columns,
    "coefficient_minutes": model.coef_,
}).sort_values("coefficient_minutes", ascending=False)

print("\n【各項目の回帰係数】")
print(coefficient_table.round(3).to_string(index=False))
print(f"切片: {model.intercept_:.3f}分")


# 実際の配達時間と予測時間を比較する表を作ります。
results = X_test.copy()
results["actual_minutes"] = y_test
results["predicted_minutes"] = predicted
results["error_minutes"] = predicted - y_test

print("\n【予測結果：先頭10件】")
print(results.head(10).round(1))


# 新しい注文の例を作り、到着予定時間を予測します。
new_order = pd.DataFrame({
    "distance_km": [5.5],
    "item_count": [3],
    "restaurant_prep_minutes": [18.0],
    "traffic_level": [3],
    "is_raining": [1],
    "courier_active_orders": [2],
})
new_prediction = model.predict(new_order)[0]

print("\n【新しい注文の予測】")
print(new_order)
print(f"予想到着時間: 注文から約{new_prediction:.0f}分後")
print(f"通常の誤差幅を考慮した案内例: 約{new_prediction - mae:.0f}〜"
      f"{new_prediction + mae:.0f}分後")


# 左：実測値と予測値、右：予測値と残差を表示します。
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


# 残差は「実測値 - 予測値」です。0付近へランダムに散らばるのが理想です。
residuals = y_test - predicted
axes[1].scatter(predicted, residuals, alpha=0.7, color="#54A24B")
axes[1].axhline(0, color="#E45756", linestyle="--")
axes[1].set_xlabel("Predicted delivery time (minutes)")
axes[1].set_ylabel("Residual: actual - predicted (minutes)")
axes[1].set_title("Residual Plot")
axes[1].grid(alpha=0.25)

fig.tight_layout()
plt.show()


print("\n【実務上の注意】")
print("予測値は確定時刻ではありません。交通事故、店舗混雑、住所確認など、")
print("データにない要因でも遅れるため、幅を持たせて案内することが重要です。")

