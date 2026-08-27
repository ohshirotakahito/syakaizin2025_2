# -*- coding: utf-8 -*-
"""
演習：未知の分光試料をPCAとクラスタリングで探索する（解答版）

【想定する場面】
原料倉庫から、仕入先情報が付いていない60個の試料が見つかりました。
各試料の分光スペクトルをPCAで2次元へ要約し、似ている試料を
k-meansとDBSCANでグループ分けします。

PCAもクラスタリングも、正解ラベルを学習に使わない教師なし学習です。
クラスタ番号は計算上の番号であり、仕入先名や品質順位ではありません。
"""

# matplotlib：スペクトルやクラスタ結果を表示します。
import matplotlib.pyplot as plt

# NumPy：波長軸、スペクトル、配列、乱数を扱います。
import numpy as np

# KMeansはクラスタ数を先に指定し、中心に近いデータをまとめます。
# DBSCANは点の密集度からグループと外れ値を探します。
from sklearn.cluster import DBSCAN, KMeans

# PCA：351波長を2つの主成分へ要約します。
from sklearn.decomposition import PCA

# ARIは2通りのグループ分けの一致度、silhouetteはまとまり具合を評価します。
from sklearn.metrics import adjusted_rand_score, silhouette_score

# StandardScaler：波長ごとの尺度を揃えます。
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 3種類の模擬スペクトルを作る
# =============================================================================

rng = np.random.default_rng(7)
wavelengths = np.linspace(400, 750, 351)

# 模擬データを作るための仕入先名と代表ピークです。
# クラスタリング処理にはsupplier_namesやtrue_labelsを渡しません。
supplier_names = ["Supplier A", "Supplier B", "Supplier C"]
peak_centers = [465, 535, 620]

spectra = []
true_labels = []

for supplier_id, peak_center in enumerate(peak_centers):
    for _ in range(20):
        shifted_center = rng.normal(loc=peak_center, scale=4.0)
        exponent = -((wavelengths - shifted_center) ** 2) / (2 * 28.0 ** 2)
        ideal_spectrum = np.exp(exponent)
        noise = rng.normal(loc=0.0, scale=0.02, size=wavelengths.size)
        measured_spectrum = ideal_spectrum + noise

        spectra.append(measured_spectrum)
        true_labels.append(supplier_id)

X = np.asarray(spectra)
true_labels = np.asarray(true_labels)

print("【模擬スペクトル】")
print(f"データの形: {X.shape}（試料数, 波長数）")


# =============================================================================
# 2. 標準化してPCAを実行する
# =============================================================================

scaler = StandardScaler()
standardized_X = scaler.fit_transform(X)

pca = PCA(n_components=2)
pca_scores = pca.fit_transform(standardized_X)

explained_ratios = pca.explained_variance_ratio_
print("PCA寄与率:", explained_ratios.round(3))
print(f"第1・第2主成分の累積寄与率: {explained_ratios.sum():.3f}")


# =============================================================================
# 3. k-meansで3クラスタに分ける
# =============================================================================

# k-meansではクラスタ数を事前に指定します。
# n_init=10は初期中心を変えて10回試し、良い結果を採用する指定です。
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(pca_scores)

# シルエット係数は-1～1で、一般に大きいほどクラスタが分離しています。
kmeans_silhouette = silhouette_score(pca_scores, kmeans_labels)


# =============================================================================
# 4. DBSCANで密度に基づくクラスタリングを行う
# =============================================================================

# eps=2.0は「近く」とみなす距離、min_samples=4は密集と判断する最小点数です。
# DBSCANはクラスタ数を指定せず、孤立した点を-1（ノイズ）にできます。
dbscan = DBSCAN(eps=2.0, min_samples=4)
dbscan_labels = dbscan.fit_predict(pca_scores)

dbscan_values, dbscan_counts = np.unique(dbscan_labels, return_counts=True)

# 今回は2つ以上のクラスタが得られたため、シルエット係数を計算できます。
non_noise_mask = dbscan_labels != -1
non_noise_labels = dbscan_labels[non_noise_mask]

if len(np.unique(non_noise_labels)) >= 2:
    dbscan_silhouette = silhouette_score(
        pca_scores[non_noise_mask],
        non_noise_labels,
    )
else:
    dbscan_silhouette = None


# =============================================================================
# 5. 模擬データの作成時ラベルと比較する
# =============================================================================

# 実際の未知試料には正解がありませんが、模擬データでは作成元が分かります。
# ARIはクラスタ番号の付け方に影響されず、1なら2つの分け方が完全一致です。
kmeans_ari = adjusted_rand_score(true_labels, kmeans_labels)
dbscan_ari = adjusted_rand_score(true_labels, dbscan_labels)

print("\n【クラスタリング結果】")
print(f"k-means シルエット係数: {kmeans_silhouette:.3f}")
print(f"k-means ARI: {kmeans_ari:.3f}")
print("DBSCAN ラベルと件数:", dict(zip(dbscan_values, dbscan_counts)))

if dbscan_silhouette is None:
    print("DBSCAN：クラスタが2つ未満のためシルエット係数を計算できません。")
else:
    print(f"DBSCAN シルエット係数: {dbscan_silhouette:.3f}")

print(f"DBSCAN ARI: {dbscan_ari:.3f}")


# =============================================================================
# 6. 作成元、k-means、DBSCANを同じ座標で比較する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(16, 5), sharex=True, sharey=True)

plots = [
    (true_labels, "Known source (simulation only)", "viridis"),
    (kmeans_labels, "k-means clusters", "viridis"),
    (dbscan_labels, "DBSCAN clusters", "tab10"),
]

for axis, (colors, title, color_map) in zip(axes, plots):
    scatter = axis.scatter(
        pca_scores[:, 0],
        pca_scores[:, 1],
        c=colors,
        cmap=color_map,
        s=65,
        alpha=0.8,
        edgecolor="white",
    )
    axis.set_title(title)
    axis.set_xlabel(f"PC1 ({explained_ratios[0]:.1%})")
    axis.set_ylabel(f"PC2 ({explained_ratios[1]:.1%})")
    axis.grid(alpha=0.25)

# DBSCANの-1は外れ候補です。ただし、異常品と確定した意味ではありません。
figure.suptitle("PCA Visualization and Clustering Comparison")
figure.tight_layout()
plt.show()


# =============================================================================
# 結果を使うときの注意
# =============================================================================

print("\n注意：クラスタ番号0、1、2自体に大小・良否・仕入先名の意味はありません。")
print("DBSCANの結果はepsとmin_samplesに大きく影響されます。")
print("実務では原料記録、標準試料、再測定結果と照合してグループを解釈します。")
