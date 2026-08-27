# -*- coding: utf-8 -*-
"""
D1 演習課題8（問題版）：観光地域を分析して施策を提案しよう
====================================================

【この課題で行うこと】
あなたは広域観光組織のデータ分析担当者です。40地域について、訪問者数、
消費額、宿泊数、外国人比率、季節変動、満足度という6指標を分析します。

最初にPCAで6指標をPC1・PC2の2軸へ要約し、地域の位置を見やすくします。
次にk-meansで特徴が似た地域をグループ化し、各グループへ施策を提案します。

【6つの指標】
・annual_visitors_10k      ：年間訪問者数（万人）
・spend_per_person_yen     ：1人あたり観光消費額（円）
・average_nights           ：平均宿泊数（泊）
・foreign_visitor_percent  ：外国人訪問者の割合（%）
・seasonality_index        ：季節による変動の大きさ（0～1）
・satisfaction_5           ：満足度（1～5）

【用語】
・PCA：多くの指標の情報を、少数の総合的な軸へ要約する方法
・寄与率：各主成分が元の情報をどれくらい説明できるかを表す割合
・k-means：特徴が似たデータを、指定した数のクラスタへ分ける方法
・シルエット係数：クラスタのまとまり具合を表す値。大きいほど分かれ方が明確
・クラスタ中心：各グループの平均的な特徴を表す値

【取り組み方】
コードをすべて一から書く必要はありません。選択肢を読み、「____」だけを
埋めてください。データの整形、地域像の命名、施策、グラフ描画は完成コードを
用意しています。

注意：「____」が残っている間は、プログラムは正しく実行できません。
データは演習用に生成した架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# ==================================================================
# 準備：4種類を想定した40地域の架空データを作る
# ==================================================================
rng = np.random.default_rng(42)

# 6指標の代表値です。上から都市型、滞在型、季節型、地域発見型を想定します。
profiles = np.array([
    [185, 22000, 1.4, 42, 0.22, 4.0],
    [95, 32000, 3.8, 24, 0.30, 4.5],
    [72, 18000, 2.1, 12, 0.82, 4.2],
    [38, 14500, 1.7, 7, 0.38, 4.4],
])
noise_scales = np.array([12, 1800, 0.25, 3.5, 0.05, 0.12])

generated_rows = []
for profile in profiles:
    generated_rows.append(rng.normal(profile, noise_scales, size=(10, 6)))
generated_data = np.vstack(generated_rows)

tourism = pd.DataFrame(generated_data, columns=[
    "annual_visitors_10k",
    "spend_per_person_yen",
    "average_nights",
    "foreign_visitor_percent",
    "seasonality_index",
    "satisfaction_5",
])
tourism.insert(0, "region", [f"Tourism-{n:02d}" for n in range(1, 41)])

# 解答版と同じ表示桁・値の範囲へ整えます。この前処理は変更しないでください。
tourism["annual_visitors_10k"] = tourism["annual_visitors_10k"].round(1)
tourism["spend_per_person_yen"] = (
    tourism["spend_per_person_yen"].round().astype(int)
)
tourism["average_nights"] = tourism["average_nights"].round(2)
tourism["foreign_visitor_percent"] = tourism["foreign_visitor_percent"].round(1)
tourism["seasonality_index"] = tourism["seasonality_index"].clip(0, 1).round(2)
tourism["satisfaction_5"] = tourism["satisfaction_5"].clip(1, 5).round(2)

print("【観光地域データ】")
print(tourism.head())
print("\n【各指標の平均と標準偏差】")
print(tourism.drop(columns="region").agg(["mean", "std"]).round(2))


# 【確認問題1】seasonality_indexが大きい地域の説明はどれですか。
# A. 季節による訪問者数の変動が大きい
# B. 必ず満足度が低い
# C. 外国人観光客がいない
# 自分の答え：


# ==================================================================
# 問題1：地域名を除いた6指標を取り出そう
# ==================================================================
# regionは地域を識別する文字列なので、PCAやk-meansの数値計算には使いません。
# columns.drop()でregion以外の列名を取り出します。
#
# 選択肢：A. "region"    B. "PC1"    C. "cluster"
# 自分の答え：
feature_names = tourism.columns.drop(____)
features = tourism[feature_names]


# ==================================================================
# 問題2：6指標を標準化しよう
# ==================================================================
# 消費額は数万円、宿泊数は数泊なので、単位と数値の大きさが違います。
# StandardScalerで同じ尺度へそろえ、特定の項目だけが強く影響するのを防ぎます。
#
# 問題2-A：標準化を行うクラス名を選んでください。
# 選択肢：A. StandardScaler    B. KMeans    C. PCA
# 自分の答え：
scaler = ____()

# 問題2-B：標準化の計算と変換を行うメソッドを選んでください。
# 選択肢：A. fit_transform    B. inverse_transform    C. idxmax
# 自分の答え：
scaled_features = scaler.____(features)


# 【確認問題2】標準化する主な理由はどれですか。
# A. 円、泊、割合など異なる尺度を公平に扱うため
# B. 地域数を増やすため
# C. 地域名を英語へ翻訳するため
# 自分の答え：


# ==================================================================
# 問題3：PCAで6指標をPC1・PC2へ要約しよう
# ==================================================================
# n_componentsは、いくつの主成分へ要約するかを表します。今回はグラフで
# 表示できるよう、PC1とPC2の2つにします。
#
# 問題3-A：「____」へ入る数を選んでください。
# 選択肢：A. 2    B. 6    C. 40
# 自分の答え：
pca = PCA(n_components=____)

# 問題3-B：PCAを学習し、各地域を2次元へ変換するメソッドを選んでください。
# 選択肢：A. fit_transform    B. value_counts    C. drop
# 自分の答え：
points = pca.____(scaled_features)

print("\n【PCAの寄与率】")
print(f"PC1: {pca.explained_variance_ratio_[0]:.1%}")
print(f"PC2: {pca.explained_variance_ratio_[1]:.1%}")
print(f"累積: {pca.explained_variance_ratio_.sum():.1%}")


# 【確認問題3】PCAを使う主な目的はどれですか。
# A. 多数の指標を、情報をできるだけ保ちながら少数の軸へ要約する
# B. 地域を正解と不正解へ分ける
# C. 観光客数の将来値を直接予測する
# 自分の答え：


# ==================================================================
# 問題4：クラスタ数を2～6まで比較しよう
# ==================================================================
# k-meansでは、クラスタ数kを事前に指定します。ここではk=2～6を試し、
# シルエット係数が最も高いkを採用します。
k_candidates = range(2, 7)
scores = []

for k in k_candidates:
    # 問題4-A：現在試しているクラスタ数を指定してください。
    # 選択肢：A. k    B. 40    C. "region"
    candidate = KMeans(n_clusters=____, random_state=42, n_init=10)
    labels = candidate.fit_predict(scaled_features)

    # 問題4-B：まとまり具合を評価する関数名を選んでください。
    # 選択肢：A. silhouette_score    B. StandardScaler    C. argmax
    score = ____(scaled_features, labels)
    scores.append(score)
    print(f"k={k}: シルエット係数={score:.3f}")


# np.argmax()で最大のスコアがある位置を探します。
# 選択肢：A. argmax    B. mean    C. append
# 自分の答え：
best_k = list(k_candidates)[int(np.____(scores))]
print(f"採用クラスタ数: {best_k}")


# 【確認問題4】シルエット係数について正しい説明はどれですか。
# A. 大きいほど、同じクラスタ内がまとまり、別クラスタから離れている
# B. 小さいほど、分類の正解率が高い
# C. 観光消費額の平均を表す
# 自分の答え：


# ==================================================================
# 問題5：選んだクラスタ数で最終分類を行おう
# ==================================================================
# 問題5-A：最終モデルのクラスタ数へ入れる変数を選んでください。
# 選択肢：A. best_k    B. k_candidates    C. scores
# 自分の答え：
model = KMeans(n_clusters=____, random_state=42, n_init=10)

# 問題5-B：学習とクラスタ割り当てを行うメソッドを選んでください。
# 選択肢：A. fit_predict    B. inverse_transform    C. round
# 自分の答え：
clusters = model.____(scaled_features)


# ==================================================================
# 問題6：クラスタ中心を元の単位へ戻そう
# ==================================================================
# model.cluster_centers_は標準化後の値です。消費額を円、宿泊数を泊として
# 解釈できるよう、StandardScalerで元の単位へ戻します。
#
# 選択肢：A. fit_transform    B. inverse_transform    C. value_counts
# 自分の答え：
centers = pd.DataFrame(
    scaler.____(model.cluster_centers_),
    columns=feature_names,
)


# 【確認問題5】クラスタ中心を元の単位へ戻す理由はどれですか。
# A. 平均消費額や宿泊数として、人が解釈しやすくするため
# B. クラスタ数を増やすため
# C. PCAを取り消すため
# 自分の答え：


# ==================================================================
# 準備：クラスタ中心から4つの地域像へ名前を付けよう
# ==================================================================
# クラスタ番号自体に順位や意味はありません。中心値の特徴から名前を付けます。
# この判定処理は記入済みです。

# 年間訪問者数が最大：都市の玄関口型
urban = centers["annual_visitors_10k"].idxmax()
remaining = centers.drop(index=urban)

# 残りの中で平均宿泊数が最大：滞在型リゾート
resort = remaining["average_nights"].idxmax()
remaining = remaining.drop(index=resort)

# 残りの中で季節変動が最大：季節型自然観光
seasonal = remaining["seasonality_index"].idxmax()

# 最後に残ったもの：地域発見型
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


# 【確認問題6】地域像と説明の正しい組み合わせはどれですか。
# A. Urban Gateway：年間訪問者数が多い都市の玄関口型
# B. Stay Resort：平均宿泊数が最も少ない地域
# C. Seasonal Nature：季節変動が最も小さい地域
# 自分の答え：


# ==================================================================
# 準備：地域像ごとの施策例を表示しよう
# ==================================================================
strategies = {
    "Urban Gateway": "混雑分散、地方周遊への送客、多言語案内",
    "Stay Resort": "連泊商品、高付加価値体験、リピーター施策",
    "Seasonal Nature": "閑散期イベント、通年コンテンツ、予約平準化",
    "Local Discovery": "認知向上、交通案内、地域文化の物語化",
}

print("\n【推奨施策】")
for segment, strategy in strategies.items():
    print(f"{segment:16s}: {strategy}")


# ==================================================================
# 準備：クラスタ数と地域分布をグラフで確認しよう
# ==================================================================
# 描画コードは複雑なので記入済みです。左はkごとのシルエット係数、右は
# PCAで2次元にした地域をセグメント別に色分けしたグラフです。
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
    "Urban Gateway": "#4C78A8",
    "Stay Resort": "#E45756",
    "Seasonal Nature": "#F2CF5B",
    "Local Discovery": "#54A24B",
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


# ==================================================================
# 最後の考察
# ==================================================================
# 1. 訪問者数が多い地域を、単純に「優れた地域」と判断してよいでしょうか。
#    混雑、住民生活、自然環境、観光収入の地域還元も考えて答えてください。
# 自分の答え：


# 2. 今回の6指標以外に追加したい情報を2つ以上選んでください。
# A. 住民満足度    B. 混雑度    C. 観光による環境負荷
# D. 地域名の文字数    E. ファイルの保存時刻
# 自分の答え：


# 3. データ分析の提案と現地関係者の意見が異なる場合、どのように意思決定
#    するとよいでしょうか。現地調査、対話、試行的な施策も考えてください。
# 自分の答え：


print("\n【注意】")
print("分類は施策検討の出発点です。同じグループでも地域文化や住民の意向は")
print("異なるため、現地調査と対話を組み合わせて最終判断します。")
