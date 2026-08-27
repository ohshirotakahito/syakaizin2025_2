# -*- coding: utf-8 -*-
"""
D1 演習課題4（解答版）：購買履歴から顧客施策を考えよう
====================================================

【設定】
あなたはECサイトのCRM（顧客関係管理）担当者です。全員へ同じクーポンを
送るのではなく、購買行動が似た顧客をグループ化し、それぞれに適した施策を
実施したいと考えています。

正解ラベルは存在しないため、教師なし学習のk-meansを使用します。
クラスタ数を評価し、各クラスタの平均的な顧客像から名前を付けます。
"""

# グラフ描画に使用します。
import matplotlib.pyplot as plt

# 数値計算に使用します。
import numpy as np

# 表形式のデータ作成と集計に使用します。
import pandas as pd

# k-meansによるクラスタリングに使用します。
from sklearn.cluster import KMeans

# 多次元の顧客データを2次元グラフへ要約するために使用します。
from sklearn.decomposition import PCA

# クラスタのまとまり具合を評価するシルエット係数を計算します。
from sklearn.metrics import silhouette_score

# 単位の異なる3項目を公平に比較できるよう標準化します。
from sklearn.preprocessing import StandardScaler


# 32人の架空顧客について、過去1年間の購買履歴を用意します。
# annual_orders    : 過去1年間の注文回数
# avg_order_yen    : 1回あたり平均注文額（円）
# days_since_last  : 最終購入からの経過日数（日、小さいほど最近購入）
customers = pd.DataFrame({
    "customer_id": [f"C{number:03d}" for number in range(1, 33)],
    "annual_orders": [
        24, 28, 21, 30, 19, 26, 23, 27,
        32, 38, 29, 35, 40, 31, 36, 34,
        6, 8, 5, 9, 7, 4, 10, 6,
        2, 5, 3, 6, 1, 4, 3, 5,
    ],
    "avg_order_yen": [
        16800, 19200, 14500, 21800, 13200, 18400, 15700, 20500,
        3200, 4100, 2800, 4600, 3500, 3900, 4300, 3000,
        18500, 22000, 15800, 24500, 19800, 17200, 23100, 21000,
        3800, 6200, 2900, 7100, 2400, 5400, 4500, 6800,
    ],
    "days_since_last": [
        8, 3, 14, 2, 18, 6, 11, 4,
        5, 2, 9, 3, 1, 7, 4, 6,
        145, 110, 190, 95, 130, 220, 88, 165,
        75, 42, 120, 35, 180, 65, 98, 50,
    ],
})


print("【顧客データ：先頭5行】")
print(customers.head())


# customer_idは識別用の文字列なので、機械学習へは渡しません。
# 3つの数値列だけをfeaturesへ取り出します。
feature_names = ["annual_orders", "avg_order_yen", "days_since_last"]
features = customers[feature_names]


# 注文額は数万円、注文回数は数十回なので、単位と桁が異なります。
# StandardScalerで、各列を平均0・標準偏差1の尺度へ変換します。
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)


# 適切なクラスタ数を考えるため、2から6クラスタまで試します。
# シルエット係数は-1から1の範囲で、大きいほどクラスタ内がまとまり、
# 異なるクラスタ同士が離れていることを表します。
candidate_k = range(2, 7)
silhouette_scores = []

for k in candidate_k:
    # 比較するすべてのkで同じ条件になるよう設定します。
    candidate_model = KMeans(n_clusters=k, random_state=42, n_init=10)

    # 各顧客をクラスタへ割り当てます。
    candidate_labels = candidate_model.fit_predict(scaled_features)

    # 標準化空間でのシルエット係数を計算し、リストへ追加します。
    score = silhouette_score(scaled_features, candidate_labels)
    silhouette_scores.append(score)
    print(f"クラスタ数={k}: シルエット係数={score:.3f}")


# np.argmax()は最大値がある位置を返します。
# その位置をcandidate_kへ対応させ、最も評価の高いクラスタ数を選びます。
best_k = list(candidate_k)[int(np.argmax(silhouette_scores))]
print(f"\n採用するクラスタ数: {best_k}")


# 選んだクラスタ数で最終モデルを学習します。
model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
cluster_numbers = model.fit_predict(scaled_features)


# 標準化されたクラスタ中心を、inverse_transform()で円・回・日の
# 元の単位へ戻します。これにより各クラスタの顧客像を解釈できます。
centers_original = scaler.inverse_transform(model.cluster_centers_)
cluster_summary = pd.DataFrame(centers_original, columns=feature_names)

# value_counts()で各クラスタの人数を数え、クラスタ番号順に追加します。
cluster_summary["customers"] = (
    pd.Series(cluster_numbers).value_counts().sort_index().to_numpy()
)


# k-meansの番号は無作為なので、中心値を使って実務向けの名前を付けます。
# 最終購入からの日数が最も長いクラスタを「休眠・離反注意」とします。
dormant_cluster = cluster_summary["days_since_last"].idxmax()

# 休眠クラスタを除き、平均注文額が最も高いものを「優良VIP」とします。
remaining = cluster_summary.drop(index=dormant_cluster)
vip_cluster = remaining["avg_order_yen"].idxmax()

# 残った中で注文回数が最も多いものを「頻繁・お手頃」とします。
remaining = remaining.drop(index=vip_cluster)
frequent_cluster = remaining["annual_orders"].idxmax()

# 最後に残ったクラスタを「育成候補」とします。
developing_cluster = remaining.drop(index=frequent_cluster).index[0]

persona_by_cluster = {
    dormant_cluster: "Dormant / Win-back",
    vip_cluster: "Loyal VIP",
    frequent_cluster: "Frequent / Value",
    developing_cluster: "Developing",
}


# 各顧客へクラスタ番号と顧客像の名前を追加します。
customers["cluster"] = cluster_numbers
customers["persona"] = customers["cluster"].map(persona_by_cluster)
cluster_summary["persona"] = cluster_summary.index.map(persona_by_cluster)

print("\n【クラスタごとの平均的な顧客像】")
print(cluster_summary.set_index("persona").round(1))


# 顧客像ごとに考えられる施策例を用意します。
actions = {
    "Loyal VIP": "先行販売、限定商品、VIP会員特典",
    "Frequent / Value": "まとめ買い割引、送料無料条件の提案",
    "Dormant / Win-back": "再購入クーポン、離反理由アンケート",
    "Developing": "初回購入後のフォロー、関連商品の紹介",
}

print("\n【顧客像ごとの施策例】")
for persona, action in actions.items():
    count = (customers["persona"] == persona).sum()
    print(f"{persona:22s} ({count}人): {action}")


# 1つ目のグラフ：クラスタ数とシルエット係数の関係を描きます。
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(list(candidate_k), silhouette_scores, marker="o", color="#4C78A8")
axes[0].axvline(best_k, color="#E45756", linestyle="--",
                label=f"Selected k = {best_k}")
axes[0].set_xlabel("Number of clusters (k)")
axes[0].set_ylabel("Silhouette score")
axes[0].set_title("Selecting the Number of Customer Segments")
axes[0].set_xticks(list(candidate_k))
axes[0].grid(alpha=0.25)
axes[0].legend()


# 3項目のデータをPCAで2次元へ要約し、散布図で見えるようにします。
pca = PCA(n_components=2)
points_2d = pca.fit_transform(scaled_features)

# 顧客像ごとに色を固定し、凡例を分かりやすくします。
persona_colors = {
    "Loyal VIP": "#E45756",
    "Frequent / Value": "#4C78A8",
    "Dormant / Win-back": "#B279A2",
    "Developing": "#54A24B",
}

for persona, color in persona_colors.items():
    selected = customers["persona"] == persona
    axes[1].scatter(points_2d[selected, 0], points_2d[selected, 1],
                    color=color, s=75, alpha=0.85, label=persona)

# 各点へ顧客IDを表示し、元データと照合できるようにします。
for index, customer_id in enumerate(customers["customer_id"]):
    axes[1].annotate(customer_id, points_2d[index], xytext=(4, 3),
                     textcoords="offset points", fontsize=7)

axes[1].set_xlabel("PCA component 1")
axes[1].set_ylabel("PCA component 2")
axes[1].set_title("Customer Segments")
axes[1].grid(alpha=0.25)
axes[1].legend(title="Recommended action group", fontsize=8)

fig.tight_layout()
plt.show()


print("\n【注意】")
print("クラスタは施策を考える手掛かりであり、顧客の価値を決めるものではありません。")
print("実務では定期的に再学習し、施策後の反応も検証する必要があります。")

