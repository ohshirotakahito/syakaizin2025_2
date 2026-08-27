# -*- coding: utf-8 -*-
"""
D1 演習課題8（解答版）：観光地域を分析して施策を提案しよう
====================================================

あなたは広域観光組織のデータ分析担当者です。40地域の観光実績をPCAで
見える化し、k-meansで似た地域を分類して、グループ別の施策を提案します。
データは演習用に生成した架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


rng = np.random.default_rng(42)


# 4種類の観光地域について、6指標の代表値を設定します。
# 順番：年間訪問者、消費額、宿泊数、外国人比率、季節変動、満足度
profiles = np.array([
    [185, 22000, 1.4, 42, 0.22, 4.0],  # 都市ゲートウェイ
    [95, 32000, 3.8, 24, 0.30, 4.5],   # 滞在型リゾート
    [72, 18000, 2.1, 12, 0.82, 4.2],   # 季節型自然観光
    [38, 14500, 1.7, 7, 0.38, 4.4],    # 地域発見型
])
noise_scales = np.array([12, 1800, 0.25, 3.5, 0.05, 0.12])


# 各タイプ10地域、合計40地域を代表値の周辺に生成します。
generated_rows = []
for profile in profiles:
    generated_rows.append(rng.normal(profile, noise_scales, size=(10, 6)))
generated_data = np.vstack(generated_rows)

tourism = pd.DataFrame(generated_data, columns=[
    "annual_visitors_10k", "spend_per_person_yen", "average_nights",
    "foreign_visitor_percent", "seasonality_index", "satisfaction_5",
])
tourism.insert(0, "region", [f"Tourism-{n:02d}" for n in range(1, 41)])

# 値を現実的な表示桁へ丸めます。
tourism["annual_visitors_10k"] = tourism["annual_visitors_10k"].round(1)
tourism["spend_per_person_yen"] = tourism["spend_per_person_yen"].round().astype(int)
tourism["average_nights"] = tourism["average_nights"].round(2)
tourism["foreign_visitor_percent"] = tourism["foreign_visitor_percent"].round(1)
tourism["seasonality_index"] = tourism["seasonality_index"].clip(0, 1).round(2)
tourism["satisfaction_5"] = tourism["satisfaction_5"].clip(1, 5).round(2)

print("【観光地域データ】")
print(tourism.head())


# 地域名を除いた6つの数値指標を標準化します。
feature_names = tourism.columns.drop("region")
features = tourism[feature_names]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)


# まずPCAで6次元から2次元へ要約します。
pca = PCA(n_components=2)
points = pca.fit_transform(scaled_features)
print("\n【PCAの寄与率】")
print(f"PC1: {pca.explained_variance_ratio_[0]:.1%}")
print(f"PC2: {pca.explained_variance_ratio_[1]:.1%}")
print(f"累積: {pca.explained_variance_ratio_.sum():.1%}")


# 2〜6クラスタを比較し、シルエット係数最大のkを採用します。
k_candidates = range(2, 7)
scores = []
for k in k_candidates:
    candidate = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = candidate.fit_predict(scaled_features)
    score = silhouette_score(scaled_features, labels)
    scores.append(score)
    print(f"k={k}: シルエット係数={score:.3f}")

best_k = list(k_candidates)[int(np.argmax(scores))]
print(f"採用クラスタ数: {best_k}")


# 選択したkで最終的なクラスタリングを行います。
model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
clusters = model.fit_predict(scaled_features)

# クラスタ中心を元の単位へ戻し、各グループを解釈します。
centers = pd.DataFrame(
    scaler.inverse_transform(model.cluster_centers_), columns=feature_names
)

# 番号には意味がないため、中心値の特徴から実務的な名前を付けます。
urban = centers["annual_visitors_10k"].idxmax()
remaining = centers.drop(index=urban)
resort = remaining["average_nights"].idxmax()
remaining = remaining.drop(index=resort)
seasonal = remaining["seasonality_index"].idxmax()
local = remaining.drop(index=seasonal).index[0]

segment_names = {
    urban: "Urban Gateway",
    resort: "Stay Resort",
    seasonal: "Seasonal Nature",
    local: "Local Discovery",
}
tourism["cluster"] = clusters
tourism["segment"] = tourism["cluster"].map(segment_names)
centers["segment"] = centers.index.map(segment_names)
centers["regions"] = pd.Series(clusters).value_counts().sort_index().to_numpy()

print("\n【セグメント別の平均像】")
print(centers.set_index("segment").round(2))


strategies = {
    "Urban Gateway": "混雑分散、地方周遊への送客、多言語案内",
    "Stay Resort": "連泊商品、高付加価値体験、リピーター施策",
    "Seasonal Nature": "閑散期イベント、通年コンテンツ、予約平準化",
    "Local Discovery": "認知向上、交通案内、地域文化の物語化",
}
print("\n【推奨施策】")
for segment, strategy in strategies.items():
    print(f"{segment:16s}: {strategy}")


# 左にkの評価、右にPCA上の地域セグメントを表示します。
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
axes[0].plot(list(k_candidates), scores, marker="o", color="#4C78A8")
axes[0].axvline(best_k, color="#E45756", linestyle="--",
                label=f"Selected k={best_k}")
axes[0].set_xlabel("Number of clusters")
axes[0].set_ylabel("Silhouette score")
axes[0].set_title("Cluster Number Selection")
axes[0].set_xticks(list(k_candidates))
axes[0].grid(alpha=0.25)
axes[0].legend()

colors = {
    "Urban Gateway": "#4C78A8", "Stay Resort": "#E45756",
    "Seasonal Nature": "#F2CF5B", "Local Discovery": "#54A24B",
}
for segment, color in colors.items():
    selected = tourism["segment"] == segment
    axes[1].scatter(points[selected, 0], points[selected, 1],
                    color=color, s=75, alpha=0.85, label=segment)

for index, region in enumerate(tourism["region"]):
    axes[1].annotate(region, points[index], xytext=(3, 3),
                     textcoords="offset points", fontsize=6.5)

axes[1].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
axes[1].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
axes[1].set_title("Tourism Region Segments")
axes[1].grid(alpha=0.25)
axes[1].legend(fontsize=8)
fig.tight_layout()
plt.show()


print("\n【注意】")
print("分類は施策検討の出発点です。同じグループでも地域文化や住民の意向は")
print("異なるため、現地調査と対話を組み合わせて最終判断します。")

