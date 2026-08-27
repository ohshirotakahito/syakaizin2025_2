# -*- coding: utf-8 -*-
"""
D1 演習課題2（解答版）：賃貸物件データを公平に比較しよう
================================================

【あなたの役割】
あなたは、不動産ポータル会社のデータ分析担当者です。同じ沿線に掲載された
物件の特徴が似ているものを自動的にグループ分けし、検索画面で比較しやすく
する仕組みを試作しています。

【困っていること】
物件データには「家賃（円）」「広さ（平方メートル）」「駅徒歩（分）」
「築年数（年）」があります。家賃は管理費を含まない月額、広さは専有面積、
駅徒歩は最寄り駅までの徒歩分数、築年数は掲載時点の年数です。しかし、家賃は
数万から十数万という値、ほかの項目は数十程度の値です。このまま機械学習を
行うと、数値が大きい家賃ばかりが強く影響する可能性があります。

そこで、すべての項目を同じ基準で比較できるように「標準化」を行います。
標準化後は、各項目の平均がほぼ0、標準偏差がほぼ1になります。

【問題】
1. 標準化前は、4項目の値の大きさにどれくらい差がありますか。
2. StandardScalerを使って4項目を標準化してください。
3. 標準化後の平均が0、標準偏差が1に近いことを確認してください。
4. 1件目の物件は、平均的な物件と比べてどのような特徴がありますか。
5. 左右の箱ひげ図を比べ、標準化の効果を説明してください。
6. 同じデータをk-meansで分類し、標準化前後の結果を比較してください。
7. なぜ標準化前は家賃の影響が強くなりやすいのか考えてください。
8. 価格帯ラベルは表示上の整理であり、物件の品質や最終的なおすすめを
    家賃だけで決めるものではない理由を考えてください。

【選択問題の答え】
1. A：家賃はほかの項目より数値の桁が大きく、距離計算で影響しやすいためです。
2. A：StandardScalerにより、各列は平均0、標準偏差1に近い尺度になります。
3. B：家賃が全物件の平均より標準偏差1個分ほど低いことを表します。
4. C：ARIが1.0未満なら、標準化前後で一部のグループ分けが変わったと考えられます。
"""

# matplotlibは、箱ひげ図や散布図を描くためのライブラリです。
# pyplotをpltという短い名前で使用します。
import matplotlib.pyplot as plt

# pandasは、行と列を持つ表形式のデータを扱うためのライブラリです。
# DataFrameを作成したり、平均値を集計したりするために使います。
import pandas as pd

# KMeansは、特徴が似ているデータを指定した数のグループに分ける
# 教師なし機械学習の手法です。
from sklearn.cluster import KMeans

# adjusted_rand_scoreは、2通りのクラスタ分けがどれくらい一致して
# いるかを、ARIという数値で評価する関数です。
from sklearn.metrics import adjusted_rand_score

# StandardScalerは、各項目を平均0、分散1になるよう変換します。
from sklearn.preprocessing import StandardScaler


# pd.DataFrame()を使い、辞書形式のデータを行と列のある表に変換します。
# 4つのリストでは、同じ位置の値が同じ物件を表しています。
# 例えば各リストの先頭は、物件1の家賃、広さ、駅徒歩、築年数です。
#
# 列名の意味
# rent_yen     : 1か月の家賃（円）
# area_m2      : 専有面積（平方メートル）
# walk_minutes : 最寄り駅から徒歩でかかる時間（分）
# building_age : 建物が完成してからの年数（年）
properties = pd.DataFrame({
    "rent_yen": [
        72000, 85000, 115000, 68000, 132000, 94000, 78000, 105000, 62000, 148000,
        88000, 99000, 76000, 125000, 81000, 110000, 69000, 138000, 92000, 103000,
        74000, 119000, 83000, 97000, 65000, 142000, 90000, 108000, 79000, 128000,
    ],
    "area_m2": [
        24, 28, 42, 21, 55, 35, 26, 40, 19, 62,
        31, 38, 25, 50, 29, 44, 22, 58, 33, 39,
        23, 47, 27, 36, 20, 60, 32, 43, 26, 52,
    ],
    "walk_minutes": [
        8, 5, 7, 14, 4, 10, 12, 6, 18, 3,
        9, 11, 15, 5, 7, 8, 16, 4, 10, 6,
        13, 5, 9, 12, 17, 2, 8, 7, 14, 4,
    ],
    "building_age": [
        12, 8, 5, 25, 3, 15, 20, 7, 32, 2,
        10, 18, 28, 4, 14, 9, 30, 1, 16, 6,
        22, 5, 19, 13, 35, 2, 11, 8, 24, 3,
    ],
})


# head()は表の先頭5行を返します。
# まず元データを表示し、値の単位や桁数の違いを確認します。
print("【賃貸物件データ：先頭5件】")
print(properties.head())

# agg()を使うと、複数の集計処理を一度に実行できます。
# meanは平均、stdは標準偏差です。round(2)で小数第2位に丸めます。
print("\n【標準化前の平均と標準偏差】")
print(properties.agg(["mean", "std"]).round(2))


# StandardScalerの計算を行う道具を作り、scalerに代入します。
scaler = StandardScaler()

# fit_transform()は、次の2つの処理をまとめて実行します。
# fit      : 各列の平均と標準偏差をデータから学習する
# transform: 学習した値を使って各データを標準化する
# 戻り値はNumPyの配列なので、scaled_valuesという変数に保存します。
scaled_values = scaler.fit_transform(properties)

# 列名を付け直し、標準化後の配列を見やすいDataFrameに戻します。
# columns=properties.columnsにより、元データと同じ列名を使用します。
scaled_properties = pd.DataFrame(scaled_values, columns=properties.columns)

# 標準化後の平均がほぼ0、標準偏差がほぼ1か確認します。
# 小さな誤差や標準偏差の計算方法の違いにより、完全な0と1に
# ならない場合があります。
print("\n【標準化後の平均と標準偏差】")
print(scaled_properties.agg(["mean", "std"]).round(3))


# iloc[0]は、行番号0、つまり1件目の物件を取り出します。
# 標準化後の値はzスコアと呼ばれ、平均からの離れ具合を表します。
print("\n【1件目の物件の標準化後の値】")
print(scaled_properties.iloc[0].round(2))
print("正の値：全物件の平均より大きい")
print("負の値：全物件の平均より小さい")
print("0に近い値：全物件の平均に近い")


# ------------------------------------------------------------------
# 機械学習への効果を比較
# ------------------------------------------------------------------
# n_clusters=3は、物件を3グループに分けるという指定です。
# random_state=42により、実行するたびに同じ結果になります。
# n_init=10は、初期位置を変えて10回計算し、良い結果を採用する設定です。
model_before = KMeans(n_clusters=3, random_state=42, n_init=10)

# fit_predict()は、モデルの学習と各物件へのクラスタ番号の割り当てを
# 同時に行います。ここでは標準化前の元データを渡します。
clusters_before = model_before.fit_predict(properties)

# 比較のため、同じ設定のモデルをもう1つ作ります。
model_after = KMeans(n_clusters=3, random_state=42, n_init=10)

# 今度は標準化後のデータを渡してクラスタ分けします。
clusters_after = model_after.fit_predict(scaled_properties)

# k-meansのクラスタ番号は実行上の番号にすぎません。
# 各クラスタの平均家賃が低い順に、0=お手頃、1=中価格帯、
# 2=高価格帯・広めという表示上の区分へ並べ替えます。
# このラベルは検索画面用の整理であり、物件の品質評価ではありません。
def convert_to_price_tier(cluster_numbers):
    """クラスタ番号を、平均家賃順のおすすめ区分0・1・2へ変換する。"""

    # assign()で一時的にcluster列を追加し、groupby()でクラスタ別に
    # 分けた後、各クラスタの平均家賃を計算します。
    average_rents = properties.assign(cluster=cluster_numbers).groupby("cluster")[
        "rent_yen"
    ].mean()

    # sort_values()で平均家賃を安い順に並べ、そのクラスタ番号を取得します。
    cluster_order = average_rents.sort_values().index

    # 元のクラスタ番号と、新しい価格帯番号の対応表を辞書で作ります。
    # enumerate()により、安い順に0、1、2という番号が付きます。
    cluster_to_tier = {
        cluster_number: tier_number
        for tier_number, cluster_number in enumerate(cluster_order)
    }

    # map()で元の番号を価格帯番号へ置き換え、NumPy配列で返します。
    return pd.Series(cluster_numbers).map(cluster_to_tier).to_numpy()


# 標準化前後のクラスタ番号を、それぞれ価格帯番号へ変換します。
tiers_before = convert_to_price_tier(clusters_before)
tiers_after = convert_to_price_tier(clusters_after)

# グラフや表に表示する、価格帯番号と名前の対応表です。
# 実務では管理費、初期費用、間取り、日当たり、設備なども確認して判断します。
tier_names = {0: "Affordable", 1: "Standard", 2: "Premium / Spacious"}

# クラスタ番号そのものに順位や意味はないため、ARIという指標で
# 2つの分け方がどの程度一致するかを調べます（1なら完全一致）。
agreement = adjusted_rand_score(clusters_before, clusters_after)

# 元データを変更しないようcopy()で複製し、比較用の表を作ります。
comparison = properties.copy()

# 標準化前後のクラスタ番号とおすすめ区分を、新しい列として追加します。
comparison["before_cluster"] = clusters_before
comparison["after_cluster"] = clusters_after
comparison["before_tier"] = pd.Series(tiers_before).map(tier_names)
comparison["after_tier"] = pd.Series(tiers_after).map(tier_names)

print("\n【k-means：標準化前後の比較】")
print(comparison)
print(f"\n2つのクラスタ分けの一致度（ARI）: {agreement:.3f}")
print("1よりかなり小さい場合、標準化によってグループ分けが変化しています。")
print("グラフの色は各クラスタの平均家賃を基準に並べた価格帯を表します。")
print("紫=お手頃、青緑=中価格帯、黄=高級・広め、です。")

# 各クラスタの平均的な物件像を、元の単位で表示します。
print("\n【標準化なし：クラスタごとの平均】")
print(comparison.groupby("before_tier", sort=False)[properties.columns].mean().round(1))
print("\n【標準化あり：クラスタごとの平均】")
print(comparison.groupby("after_tier", sort=False)[properties.columns].mean().round(1))


# グラフ上で使用する、短く読みやすい英語の項目名を用意します。
labels = ["Rent", "Area", "Walk time", "Building age"]

# 1行2列のグラフ領域を作ります。
# figは図全体、axes[0]とaxes[1]は左右それぞれのグラフを表します。
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左側に、標準化前の4項目の箱ひげ図を描きます。
# 家賃の数値だけが非常に大きいため、ほかの箱が小さく見えます。
axes[0].boxplot(properties, tick_labels=labels, patch_artist=True)
axes[0].set_title("Before Standardization")
axes[0].set_ylabel("Original values (different units)")
axes[0].tick_params(axis="x", rotation=20)
axes[0].grid(axis="y", alpha=0.25)

# 右側に、標準化後の4項目の箱ひげ図を描きます。
# 4項目が同じ尺度になり、分布の形を公平に比較できます。
axes[1].boxplot(scaled_properties, tick_labels=labels, patch_artist=True)

# y=0の位置に赤い破線を引きます。標準化後の0は全体平均です。
axes[1].axhline(0, color="red", linestyle="--", linewidth=1, label="Mean = 0")
axes[1].set_title("After Standardization")
axes[1].set_ylabel("Standardized value (z-score)")
axes[1].tick_params(axis="x", rotation=20)
axes[1].grid(axis="y", alpha=0.25)
axes[1].legend()

fig.suptitle("Rental Property Features: Before and After Standardization")
fig.tight_layout()


# sharex=Trueとsharey=Trueにより、左右の軸の範囲を同じにします。
# これにより、2つの結果を同じ条件で比較できます。
fig2, cluster_axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)

# 左側の散布図です。横軸を駅徒歩、縦軸を家賃にします。
# 点の色には、標準化前のデータから得たおすすめ区分を指定します。
# cmap="viridis"は紫から黄色へ変化する配色です。
scatter_before = cluster_axes[0].scatter(
    properties["walk_minutes"], properties["rent_yen"],
    c=tiers_before, cmap="viridis", vmin=0, vmax=2,
    s=90, edgecolor="white"
)
cluster_axes[0].set_title("k-means Without Standardization")

# 右側も同じ物件を描きますが、色には標準化後の区分を指定します。
# 同じ番号の物件の色が左右で変われば、所属グループが変わったと分かります。
scatter_after = cluster_axes[1].scatter(
    properties["walk_minutes"], properties["rent_yen"],
    c=tiers_after, cmap="viridis", vmin=0, vmax=2,
    s=90, edgecolor="white"
)
cluster_axes[1].set_title("k-means After Standardization")

# enumerate(..., start=1)で物件番号を1から順番に作ります。
# zip()は駅徒歩と家賃を、同じ物件ごとの組にまとめます。
for property_number, (walk, rent) in enumerate(
        zip(properties["walk_minutes"], properties["rent_yen"]), start=1):
    # 同じ番号を左と右の両方のグラフに表示します。
    for ax in cluster_axes:
        # annotate()は、指定した座標の近くに文字を表示する命令です。
        ax.annotate(str(property_number), (walk, rent), xytext=(4, 4),
                    textcoords="offset points", fontsize=7)

# 左右それぞれに軸ラベル、補助線、色の凡例を追加します。
for ax, scatter in zip(cluster_axes, [scatter_before, scatter_after]):
    ax.set_xlabel("Walking time from station (minutes)")
    ax.set_ylabel("Rent (JPY)")
    ax.grid(alpha=0.25)
    # legend_elements()で、散布図に使った3色の凡例部品を作ります。
    handles, _ = scatter.legend_elements(num=[0, 1, 2])
    ax.legend(handles, ["Affordable", "Standard", "Premium / Spacious"],
              title="Recommendation tier", loc="upper right")

fig2.suptitle(f"Effect of Standardization on Clustering (ARI = {agreement:.3f})")
fig2.tight_layout()

# 作成した2つの図を画面に表示します。
plt.show()
