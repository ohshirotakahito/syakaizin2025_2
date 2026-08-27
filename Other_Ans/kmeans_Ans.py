# -*- coding: utf-8 -*-
"""解答版：宅配需要地点をk-meansで配送エリアへ分ける。"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)

# 3つの生活圏周辺にある90地点の座標と1日あたり注文数を生成します。
centers = [(2.0, 7.5, 28), (7.5, 7.0, 52), (5.0, 2.3, 38)]
rows = []
for longitude, latitude, demand in centers:
    for _ in range(30):
        rows.append([
            rng.normal(longitude, 0.8), rng.normal(latitude, 0.7),
            max(5, round(rng.normal(demand, 7))),
        ])
delivery_points = pd.DataFrame(rows, columns=["x_km", "y_km", "daily_orders"])

# 位置と需要量を公平に扱うため標準化します。
scaler = StandardScaler()
scaled = scaler.fit_transform(delivery_points)

# 2〜6エリアを比較し、シルエット係数が最大の数を採用します。
scores = {}
for k in range(2, 7):
    labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(scaled)
    scores[k] = silhouette_score(scaled, labels)
best_k = max(scores, key=scores.get)

model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
delivery_points["delivery_area"] = model.fit_predict(scaled)
area_centers = pd.DataFrame(
    scaler.inverse_transform(model.cluster_centers_),
    columns=["x_km", "y_km", "daily_orders"],
)

print("【エリア数の評価】")
for k, score in scores.items():
    print(f"k={k}: {score:.3f}")
print(f"採用エリア数: {best_k}")
print("\n【配送エリア中心と平均需要】")
print(area_centers.round(2))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(list(scores), list(scores.values()), marker="o")
axes[0].axvline(best_k, color="red", linestyle="--")
axes[0].set(title="Selecting Delivery Areas", xlabel="k", ylabel="Silhouette score")
axes[0].grid(alpha=0.25)

scatter = axes[1].scatter(
    delivery_points["x_km"], delivery_points["y_km"],
    c=delivery_points["delivery_area"], s=delivery_points["daily_orders"] * 2,
    cmap="viridis", alpha=0.75, edgecolor="white",
)
axes[1].scatter(area_centers["x_km"], area_centers["y_km"],
                marker="X", s=220, color="red", label="Candidate depots")
axes[1].set(title="Delivery Demand Areas", xlabel="East-west distance (km)",
            ylabel="North-south distance (km)")
axes[1].legend()
axes[1].grid(alpha=0.2)
fig.tight_layout()
plt.show()

print("注意：道路、河川、交通規制、拠点賃料、配達員数も最終判断に必要です。")

