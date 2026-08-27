# -*- coding: utf-8 -*-
"""
D1 演習課題3（解答版）：地域の特徴を主成分分析で要約しよう
==========================================================

【設定】
あなたは自治体の企画部門で、移住促進施策を担当しています。24地域について
所得、家賃、通勤、緑地、医療、犯罪という6つの指標があります。しかし、
6項目を一度に比較するのは大変です。

主成分分析（PCA）を使い、6項目の情報をできるだけ保ちながら2つの総合指標へ
要約します。地域の位置だけでなく、各指標が主成分へ与える影響も確認します。
"""

# グラフ描画に使用します。
import matplotlib.pyplot as plt

# 表形式のデータ作成・集計に使用します。
import pandas as pd

# PCAは、多数の項目を少数の主成分へ要約する手法です。
from sklearn.decomposition import PCA

# 単位の異なる項目を公平に扱うため、標準化に使用します。
from sklearn.preprocessing import StandardScaler


# 24の架空地域について、現実にありそうな生活関連指標を用意します。
# income_10k_yen       : 平均年収（万円）
# rent_1k_yen          : 単身向け平均家賃（千円）
# commute_minutes      : 平均通勤時間（分）
# green_space_percent  : 地域面積に占める緑地の割合（%）
# clinics_per_10k      : 人口1万人あたり診療所数
# crimes_per_1k        : 人口千人あたり犯罪認知件数
regions = pd.DataFrame({
    "region": [f"Area-{number:02d}" for number in range(1, 25)],
    "income_10k_yen": [
        610, 580, 550, 520, 490, 470, 450, 430,
        510, 480, 460, 440, 420, 400, 390, 370,
        460, 440, 410, 390, 370, 350, 340, 320,
    ],
    "rent_1k_yen": [
        132, 125, 118, 110, 105, 98, 92, 88,
        102, 96, 90, 85, 80, 76, 72, 68,
        82, 78, 73, 69, 64, 60, 57, 53,
    ],
    "commute_minutes": [
        48, 45, 43, 41, 39, 38, 36, 35,
        40, 38, 36, 34, 32, 31, 29, 28,
        34, 32, 30, 28, 26, 24, 23, 21,
    ],
    "green_space_percent": [
        8, 10, 12, 15, 18, 20, 22, 25,
        14, 17, 21, 24, 28, 31, 34, 37,
        23, 27, 32, 36, 40, 44, 48, 52,
    ],
    "clinics_per_10k": [
        8.8, 8.4, 8.1, 7.8, 7.5, 7.3, 7.0, 6.8,
        9.6, 9.2, 8.9, 8.5, 8.2, 7.9, 7.6, 7.4,
        7.1, 7.4, 7.7, 8.0, 8.3, 8.6, 8.9, 9.2,
    ],
    "crimes_per_1k": [
        12.5, 11.8, 11.0, 10.2, 9.7, 9.0, 8.5, 8.0,
        9.8, 9.2, 8.7, 8.1, 7.5, 7.0, 6.6, 6.2,
        7.8, 7.2, 6.7, 6.1, 5.6, 5.1, 4.7, 4.3,
    ],
})


# region列は地域名であり、計算に使う数値ではありません。
# drop()でregion列を除き、6つの分析項目だけをXへ取り出します。
X = regions.drop(columns="region")

print("【地域データ：先頭5行】")
print(regions.head())
print("\n【各指標の平均と標準偏差】")
print(X.agg(["mean", "std"]).round(2))


# 年収は万円、診療所数は一桁というように単位が異なります。
# StandardScalerで全項目を平均0、標準偏差1の尺度へそろえます。
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# n_components=2は、6項目を第1・第2主成分の2項目へ要約する指定です。
pca = PCA(n_components=2)

# fit_transform()で主成分の方向を学習し、各地域を2次元へ変換します。
principal_components = pca.fit_transform(X_scaled)


# 変換結果を、地域名とPC1・PC2を持つ表にします。
pca_result = pd.DataFrame(
    principal_components,
    columns=["PC1", "PC2"],
)
pca_result.insert(0, "region", regions["region"])


# 寄与率は、元の情報を各主成分がどれだけ説明できるかを表します。
explained = pca.explained_variance_ratio_
print("\n【主成分の寄与率】")
print(f"第1主成分（PC1）: {explained[0]:.1%}")
print(f"第2主成分（PC2）: {explained[1]:.1%}")
print(f"2主成分の累積寄与率: {explained.sum():.1%}")


# components_には、各指標が主成分へ与える影響の向きと強さが入ります。
# 転置（.T）し、行を指標、列を主成分とする読みやすい表にします。
loadings = pd.DataFrame(
    pca.components_.T,
    index=X.columns,
    columns=["PC1", "PC2"],
)
print("\n【主成分負荷量：絶対値が大きいほど影響が強い】")
print(loadings.round(3))


# 各主成分で影響の強い上位3項目を表示します。
# abs()で正負を無視した影響の強さを求め、nlargest()で上位を選びます。
for component in ["PC1", "PC2"]:
    important_features = loadings[component].abs().nlargest(3).index.tolist()
    print(f"{component}に強く影響する項目: {', '.join(important_features)}")


# 地域を第1・第2主成分上へ配置した散布図を作ります。
fig, ax = plt.subplots(figsize=(11, 7))
ax.scatter(pca_result["PC1"], pca_result["PC2"],
           color="#4C78A8", s=75, alpha=0.8)


# 各点に地域名を付け、どの地域か分かるようにします。
for _, row in pca_result.iterrows():
    ax.annotate(row["region"], (row["PC1"], row["PC2"]),
                xytext=(5, 4), textcoords="offset points", fontsize=8)


# 負荷量を矢印で描き、各指標が増加する方向を示します。
# scaleは、短い負荷量の矢印を見やすく拡大するための係数です。
scale = 3.2
for feature in X.columns:
    x_direction = loadings.loc[feature, "PC1"] * scale
    y_direction = loadings.loc[feature, "PC2"] * scale
    ax.arrow(0, 0, x_direction, y_direction, color="#E45756",
             alpha=0.75, head_width=0.08, length_includes_head=True)
    ax.text(x_direction * 1.12, y_direction * 1.12, feature,
            color="#B33A3A", fontsize=8, ha="center")


# 原点を示す線、軸名、タイトル、補助線を追加します。
ax.axhline(0, color="gray", linewidth=0.8)
ax.axvline(0, color="gray", linewidth=0.8)
ax.set_xlabel(f"PC1 ({explained[0]:.1%} explained)")
ax.set_ylabel(f"PC2 ({explained[1]:.1%} explained)")
ax.set_title("Regional Characteristics Summarized by PCA")
ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()


print("\n【読み取り例】")
print("矢印と同じ方向にある地域ほど、その指標が平均より高い傾向があります。")
print("反対方向にある地域は、その指標が平均より低い傾向があります。")
print("PC1やPC2の正負自体に良い・悪いという意味はありません。")

