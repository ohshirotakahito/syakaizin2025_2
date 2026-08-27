# -*- coding: utf-8 -*-
"""
D1 演習課題2（問題版）：賃貸物件データを公平に比較しよう
========================================================

【あなたの役割】
あなたは不動産ポータル会社のデータ分析担当者です。同じ沿線に掲載された
賃貸物件を、検索画面で比較しやすい3グループに分ける試作を担当しています。
家賃は管理費を含まない月額、広さは専有面積、駅徒歩は最寄り駅までの徒歩分数、
築年数は掲載時点の年数です。

物件には家賃、広さ、駅からの徒歩時間、築年数があります。単位と数値の
大きさが異なる4項目を、そのまま機械学習へ渡すと、特定の項目だけが結果を
左右するかもしれません。標準化の前後でグループ分けを比較し、検索画面に
表示するための価格帯ラベルを考えます。ただし、これは候補を整理する分析で
あり、価格だけで物件の品質やお客様への最終的なおすすめを決めるものではありません。

選択問題に答え、TODO部分へコードを記入しながら確かめてください。
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler


# このデータは完成済みです。変更せずに使用してください。
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


# ==================================================================
# 問題1：元データを確認する
# ==================================================================
# TODO 1-A：propertiesの先頭5行を表示してください。
# ヒント：表の先頭を取得するメソッドは head() です。


# TODO 1-B：4項目の平均と標準偏差を表示してください。
# ヒント：agg(["mean", "std"])を使用できます。


# 【選択問題1】
# 標準化前のデータをk-meansへ渡した場合、最も強く影響しやすい項目は
# どれでしょうか。正しいと思う選択肢を残してください。
#
# A. 家賃          B. 広さ          C. 駅徒歩          D. 築年数
#
# 自分の答え：
# 理由：


# ==================================================================
# 問題2：データを標準化する
# ==================================================================
# TODO 2-A：StandardScalerのインスタンスを作り、scalerへ代入してください。


# TODO 2-B：propertiesから平均と標準偏差を学習し、同時に標準化して、
# scaled_valuesへ代入してください。
# ヒント：scalerのfit_transform()を使用します。


# TODO 2-C：scaled_valuesをDataFrameに戻し、scaled_propertiesへ
# 代入してください。列名はpropertiesと同じものを指定します。
# ヒント：pd.DataFrame(値, columns=列名)の形です。


# TODO 2-D：標準化後の各列の平均と標準偏差を表示してください。


# 【選択問題2】
# 標準化後の各項目は、どのような値になりますか。
#
# A. 平均0、標準偏差1に近くなる
# B. 平均1、標準偏差0に近くなる
# C. すべての値が0から1の範囲になる
# D. すべての項目が同じ値になる
#
# 自分の答え：


# 【選択問題3】
# 標準化後の家賃が -1.0 の物件は、どのような物件でしょうか。
#
# A. 家賃が0円の物件
# B. 家賃が平均より標準偏差1個分ほど安い物件
# C. 家賃が平均より標準偏差1個分ほど高い物件
# D. 家賃のデータが欠けている物件
#
# 自分の答え：


# ==================================================================
# 問題3：標準化前後でk-meansを実行する
# ==================================================================
# TODO 3-A：標準化前のpropertiesを3クラスタに分類してください。
# KMeansの設定はn_clusters=3、random_state=42、n_init=10とします。
# モデルをmodel_before、予測結果をclusters_beforeへ代入してください。


# TODO 3-B：標準化後のscaled_propertiesも同じ設定で分類してください。
# モデルをmodel_after、予測結果をclusters_afterへ代入してください。


# TODO 3-C：2つの分類結果のARIを計算し、agreementへ代入してください。
# ヒント：adjusted_rand_score(分類結果1, 分類結果2)を使います。


# TODO 3-D：agreementを小数第3位まで表示してください。


# 【選択問題4】
# ARIが1.0より小さかった場合、何が分かりますか。
#
# A. k-meansの実行が失敗した
# B. すべての物件が同じクラスタになった
# C. 標準化によって一部の物件のグループ分けが変わった
# D. 家賃のデータが間違っている
#
# 自分の答え：


# ==================================================================
# 問題4：価格帯として分かりやすく表示する
# ==================================================================
# k-meansのクラスタ番号0、1、2には、大小や良し悪しの意味はありません。
# 各クラスタの平均家賃を調べ、安い順に次の名前を付ける処理を考えます。
#
# 0：Affordable（お手頃）
# 1：Standard（中価格帯）
# 2：Premium / Spacious（高価格帯・広め）
# ※ここでの名前は平均家賃による表示上の区分であり、物件の品質評価ではありません。
#
# TODO 4-A：クラスタごとの平均家賃を求めてください。
# ヒント：assign()、groupby()、mean()を組み合わせます。


# TODO 4-B：平均家賃を安い順に並べ、元のクラスタ番号を価格帯番号
# 0、1、2へ変換する処理を書いてください。


# 【考察問題1】
# 平均家賃だけで「高級・広めの物件」と判断してよいでしょうか。
# 実際の検索画面でおすすめを出すなら、追加するとよいデータを2つ以上挙げてください。
# 自分の答え：


# ==================================================================
# 問題5：結果を可視化する
# ==================================================================
# TODO 5-A：標準化前と標準化後の箱ひげ図を、横に並べてください。
# ヒント：plt.subplots(1, 2, figsize=(12, 5))を使用できます。


# TODO 5-B：横軸を駅徒歩、縦軸を家賃とする散布図を2つ作り、
# 標準化前後のクラスタを色分けして比較してください。


# TODO 5-C：軸ラベル、タイトル、凡例を追加し、plt.show()で表示してください。


# 【考察問題2】
# 標準化前後で色が変わった物件を探してください。その物件は家賃以外に
# どのような特徴があるため、所属グループが変わったと考えられますか。
# 自分の答え：


# 【発展問題】
# お客様が「家賃よりも駅からの近さを重視する」と希望した場合、
# どのように分析方法を変更するとよいでしょうか。変更によって、どの物件が
# 別グループになる可能性があるかも説明してください。
# 自分の答え：

# === 解答対応ガイド（自動照合済み） ===
#
# 【このガイドの目的】
# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、
# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。
#
# 【解答版に含まれる背景・ヒント】
# ・matplotlibは、箱ひげ図や散布図を描くためのライブラリです。
# ・pyplotをpltという短い名前で使用します。
# ・pandasは、行と列を持つ表形式のデータを扱うためのライブラリです。
# ・DataFrameを作成したり、平均値を集計したりするために使います。
# ・KMeansは、特徴が似ているデータを指定した数のグループに分ける
# ・教師なし機械学習の手法です。
# ・adjusted_rand_scoreは、2通りのクラスタ分けがどれくらい一致して
# ・いるかを、ARIという数値で評価する関数です。
# ・StandardScalerは、各項目を平均0、分散1になるよう変換します。
# ・pd.DataFrame()を使い、辞書形式のデータを行と列のある表に変換します。
# ・4つのリストでは、同じ位置の値が同じ物件を表しています。
# ・例えば各リストの先頭は、物件1の家賃、広さ、駅徒歩、築年数です。
# ・列名の意味
# ・rent_yen     : 1か月の家賃（円）
# ・area_m2      : 専有面積（平方メートル）
# ・walk_minutes : 最寄り駅から徒歩でかかる時間（分）
# ・building_age : 建物が完成してからの年数（年）
# ・head()は表の先頭5行を返します。
# ・まず元データを表示し、値の単位や桁数の違いを確認します。
# ・agg()を使うと、複数の集計処理を一度に実行できます。
# ・meanは平均、stdは標準偏差です。round(2)で小数第2位に丸めます。
# ・StandardScalerの計算を行う道具を作り、scalerに代入します。
# ・fit_transform()は、次の2つの処理をまとめて実行します。
# ・fit      : 各列の平均と標準偏差をデータから学習する
# ・transform: 学習した値を使って各データを標準化する
# ・戻り値はNumPyの配列なので、scaled_valuesという変数に保存します。
# ・列名を付け直し、標準化後の配列を見やすいDataFrameに戻します。
# ・columns=properties.columnsにより、元データと同じ列名を使用します。
# ・標準化後の平均がほぼ0、標準偏差がほぼ1か確認します。
# ・小さな誤差や標準偏差の計算方法の違いにより、完全な0と1に
# ・ならない場合があります。
# ・iloc[0]は、行番号0、つまり1件目の物件を取り出します。
# ・標準化後の値はzスコアと呼ばれ、平均からの離れ具合を表します。
# ・機械学習への効果を比較
# ・n_clusters=3は、物件を3グループに分けるという指定です。
# ・random_state=42により、実行するたびに同じ結果になります。
# ・n_init=10は、初期位置を変えて10回計算し、良い結果を採用する設定です。
# ・fit_predict()は、モデルの学習と各物件へのクラスタ番号の割り当てを
# ・同時に行います。ここでは標準化前の元データを渡します。
# ・比較のため、同じ設定のモデルをもう1つ作ります。
# ・今度は標準化後のデータを渡してクラスタ分けします。
# ・k-meansのクラスタ番号は実行上の番号にすぎません。
# ・各クラスタの平均家賃が低い順に、0=お手頃、1=中価格帯、
# ・2=高級・広めという意味のある区分へ並べ替えます。
# ・assign()で一時的にcluster列を追加し、groupby()でクラスタ別に
# ・分けた後、各クラスタの平均家賃を計算します。
# ・sort_values()で平均家賃を安い順に並べ、そのクラスタ番号を取得します。
# ・元のクラスタ番号と、新しい価格帯番号の対応表を辞書で作ります。
# ・enumerate()により、安い順に0、1、2という番号が付きます。
# ・map()で元の番号を価格帯番号へ置き換え、NumPy配列で返します。
# ・標準化前後のクラスタ番号を、それぞれ価格帯番号へ変換します。
# ・グラフや表に表示する、価格帯番号と名前の対応表です。
# ・クラスタ番号そのものに順位や意味はないため、ARIという指標で
# ・2つの分け方がどの程度一致するかを調べます（1なら完全一致）。
# ・元データを変更しないようcopy()で複製し、比較用の表を作ります。
# ・標準化前後のクラスタ番号とおすすめ区分を、新しい列として追加します。
# ・各クラスタの平均的な物件像を、元の単位で表示します。
# ・グラフ上で使用する、短く読みやすい英語の項目名を用意します。
# ・1行2列のグラフ領域を作ります。
# ・figは図全体、axes[0]とaxes[1]は左右それぞれのグラフを表します。
# ・左側に、標準化前の4項目の箱ひげ図を描きます。
# ・家賃の数値だけが非常に大きいため、ほかの箱が小さく見えます。
# ・右側に、標準化後の4項目の箱ひげ図を描きます。
# ・4項目が同じ尺度になり、分布の形を公平に比較できます。
# ・y=0の位置に赤い破線を引きます。標準化後の0は全体平均です。
# ・sharex=Trueとsharey=Trueにより、左右の軸の範囲を同じにします。
# ・これにより、2つの結果を同じ条件で比較できます。
# ・左側の散布図です。横軸を駅徒歩、縦軸を家賃にします。
# ・点の色には、標準化前のデータから得たおすすめ区分を指定します。
# ・cmap="viridis"は紫から黄色へ変化する配色です。
# ・右側も同じ物件を描きますが、色には標準化後の区分を指定します。
# ・同じ番号の物件の色が左右で変われば、所属グループが変わったと分かります。
# ・enumerate(..., start=1)で物件番号を1から順番に作ります。
# ・zip()は駅徒歩と家賃を、同じ物件ごとの組にまとめます。
# ・同じ番号を左と右の両方のグラフに表示します。
# ・annotate()は、指定した座標の近くに文字を表示する命令です。
# ・左右それぞれに軸ラベル、補助線、色の凡例を追加します。
# ・legend_elements()で、散布図に使った3色の凡例部品を作ります。
# ・作成した2つの図を画面に表示します。
#
# 【実装課題：解答版との対応順】
# TODO 01：必要なライブラリまたは機能 matplotlib.pyplot（別名 plt） を読み込んでください。
# TODO 02：必要なライブラリまたは機能 pandas（別名 pd） を読み込んでください。
# TODO 03：必要なライブラリまたは機能 sklearn.cluster.KMeans を読み込んでください。
# TODO 04：必要なライブラリまたは機能 sklearn.metrics.adjusted_rand_score を読み込んでください。
# TODO 05：必要なライブラリまたは機能 sklearn.preprocessing.StandardScaler を読み込んでください。
# TODO 06：properties を作成・更新してください。 使用する処理：pd.DataFrame。 主な指定値：'rent_yen', 'area_m2', 'walk_minutes', 'building_age', 72000, 85000, 115000, 68000, 132000, 94000, 78000, 105000。
# TODO 07：次の処理を実行してください。 使用する処理：print。 主な指定値：'【賃貸物件データ：先頭5件】'。
# TODO 08：次の処理を実行してください。 使用する処理：print, properties.head。
# TODO 09：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【標準化前の平均と標準偏差】'。
# TODO 10：次の処理を実行してください。 使用する処理：print, round, properties.agg。 主な指定値：2, 'mean', 'std'。
# TODO 11：scaler を作成・更新してください。 使用する処理：StandardScaler。
# TODO 12：scaled_values を作成・更新してください。 使用する処理：scaler.fit_transform。
# TODO 13：scaled_properties を作成・更新してください。 使用する処理：pd.DataFrame。
# TODO 14：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【標準化後の平均と標準偏差】'。
# TODO 15：次の処理を実行してください。 使用する処理：print, round, scaled_properties.agg。 主な指定値：3, 'mean', 'std'。
# TODO 16：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【1件目の物件の標準化後の値】'。
# TODO 17：次の処理を実行してください。 使用する処理：print, round。 主な指定値：2, 0。
# TODO 18：次の処理を実行してください。 使用する処理：print。 主な指定値：'正の値：全物件の平均より大きい'。
# TODO 19：次の処理を実行してください。 使用する処理：print。 主な指定値：'負の値：全物件の平均より小さい'。
# TODO 20：次の処理を実行してください。 使用する処理：print。 主な指定値：'0に近い値：全物件の平均に近い'。
# TODO 21：model_before を作成・更新してください。 使用する処理：KMeans。 主な指定値：3, 42, 10。
# TODO 22：clusters_before を作成・更新してください。 使用する処理：model_before.fit_predict。
# TODO 23：model_after を作成・更新してください。 使用する処理：KMeans。 主な指定値：3, 42, 10。
# TODO 24：clusters_after を作成・更新してください。 使用する処理：model_after.fit_predict。
# TODO 25：関数 convert_to_price_tier(cluster_numbers) を定義してください。 使用する処理：mean, to_numpy, average_rents.sort_values, enumerate, map, groupby, pd.Series, properties.assign。 主な指定値：'クラスタ番号を、平均家賃順のおすすめ区分0・1・2へ変換する。', 'rent_yen', 'cluster'。 戻り値の考え方：pd.Series(cluster_numbers).map(cluster_to_tier).to_numpy()。
# TODO 26：tiers_before を作成・更新してください。 使用する処理：convert_to_price_tier。
# TODO 27：tiers_after を作成・更新してください。 使用する処理：convert_to_price_tier。
# TODO 28：tier_names を作成・更新してください。 主な指定値：0, 1, 2, 'Affordable', 'Standard', 'Premium / Spacious'。
# TODO 29：agreement を作成・更新してください。 使用する処理：adjusted_rand_score。
# TODO 30：comparison を作成・更新してください。 使用する処理：properties.copy。
# TODO 31：指定された変数 を作成・更新してください。 主な指定値：'before_cluster'。
# TODO 32：指定された変数 を作成・更新してください。 主な指定値：'after_cluster'。
# TODO 33：指定された変数 を作成・更新してください。 使用する処理：map, pd.Series。 主な指定値：'before_tier'。
# TODO 34：指定された変数 を作成・更新してください。 使用する処理：map, pd.Series。 主な指定値：'after_tier'。
# TODO 35：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【k-means：標準化前後の比較】'。
# TODO 36：次の処理を実行してください。 使用する処理：print。
# TODO 37：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n2つのクラスタ分けの一致度（ARI）: ', '.3f'。
# TODO 38：次の処理を実行してください。 使用する処理：print。 主な指定値：'1よりかなり小さい場合、標準化によってグループ分けが変化しています。'。
# TODO 39：次の処理を実行してください。 使用する処理：print。 主な指定値：'グラフの色は各クラスタの平均家賃を基準に並べた価格帯を表します。'。
# TODO 40：次の処理を実行してください。 使用する処理：print。 主な指定値：'紫=お手頃、青緑=中価格帯、黄=高級・広め、です。'。
# TODO 41：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【標準化なし：クラスタごとの平均】'。
# TODO 42：次の処理を実行してください。 使用する処理：print, round, mean, comparison.groupby。 主な指定値：1, 'before_tier', False。
# TODO 43：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【標準化あり：クラスタごとの平均】'。
# TODO 44：次の処理を実行してください。 使用する処理：print, round, mean, comparison.groupby。 主な指定値：1, 'after_tier', False。
# TODO 45：labels を作成・更新してください。 主な指定値：'Rent', 'Area', 'Walk time', 'Building age'。
# TODO 46：fig, axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, 12, 5。
# TODO 47：次の処理を実行してください。 使用する処理：boxplot。 主な指定値：True, 0。
# TODO 48：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Before Standardization', 0。
# TODO 49：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Original values (different units)', 0。
# TODO 50：次の処理を実行してください。 使用する処理：tick_params。 主な指定値：'x', 20, 0。
# TODO 51：次の処理を実行してください。 使用する処理：grid。 主な指定値：'y', 0.25, 0。
# TODO 52：次の処理を実行してください。 使用する処理：boxplot。 主な指定値：True, 1。
# TODO 53：次の処理を実行してください。 使用する処理：axhline。 主な指定値：0, 'red', '--', 1, 'Mean = 0'。
# TODO 54：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'After Standardization', 1。
# TODO 55：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Standardized value (z-score)', 1。
# TODO 56：次の処理を実行してください。 使用する処理：tick_params。 主な指定値：'x', 20, 1。
# TODO 57：次の処理を実行してください。 使用する処理：grid。 主な指定値：'y', 0.25, 1。
# TODO 58：次の処理を実行してください。 使用する処理：legend。 主な指定値：1。
# TODO 59：次の処理を実行してください。 使用する処理：fig.suptitle。 主な指定値：'Rental Property Features: Before and After Standardization'。
# TODO 60：次の処理を実行してください。 使用する処理：fig.tight_layout。
# TODO 61：fig2, cluster_axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, True, 12, 5。
# TODO 62：scatter_before を作成・更新してください。 使用する処理：scatter。 主な指定値：'walk_minutes', 'rent_yen', 'viridis', 0, 2, 90, 'white'。
# TODO 63：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'k-means Without Standardization', 0。
# TODO 64：scatter_after を作成・更新してください。 使用する処理：scatter。 主な指定値：'walk_minutes', 'rent_yen', 'viridis', 0, 2, 90, 'white', 1。
# TODO 65：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'k-means After Standardization', 1。
# TODO 66：enumerate(zip(properties['walk_minutes'], properties['rent_yen']), start=1) を順に処理する反復を作ってください。 使用する処理：enumerate, zip, ax.annotate, str。 主な指定値：1, 'walk_minutes', 'rent_yen', 'offset points', 7, 4。
# TODO 67：zip(cluster_axes, [scatter_before, scatter_after]) を順に処理する反復を作ってください。 使用する処理：zip, ax.set_xlabel, ax.set_ylabel, ax.grid, scatter.legend_elements, ax.legend。 主な指定値：'Walking time from station (minutes)', 'Rent (JPY)', 0.25, 'Affordable', 'Standard', 'Premium / Spacious', 'Recommendation tier', 'upper right', 0, 1, 2。
# TODO 68：次の処理を実行してください。 使用する処理：fig2.suptitle。 主な指定値：'Effect of Standardization on Clustering (ARI = ', ')', '.3f'。
# TODO 69：次の処理を実行してください。 使用する処理：fig2.tight_layout。
# TODO 70：次の処理を実行してください。 使用する処理：plt.show。
#
# 【使用する名前・データ仕様】
# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。
# ・adjusted_rand_score / Affordable / After Standardization / after_cluster / after_tier / agg / agreement / annotate
# ・Area / area_m2 / assign / average_rents / axes / axhline / Before Standardization / before_cluster
# ・before_tier / boxplot / Building age / building_age / cluster / cluster_axes / cluster_number / cluster_order
# ・cluster_to_tier / clusters_after / clusters_before / comparison / convert_to_price_tier / copy / DataFrame / enumerate
# ・fig2 / fit_predict / fit_transform / grid / groupby / handles / head / k-means After Standardization
# ・k-means Without Standardization / KMeans / labels / legend / legend_elements / map / mean / model_after
# ・model_before / offset points / Premium / Spacious / properties / property_number / Recommendation tier / rent / Rent
# ・rent_yen / round / scaled_properties / scaled_values / scaler / scatter / scatter_after / scatter_before
# ・Series / set_title / set_xlabel / set_ylabel / show / sort_values / Standard / StandardScaler
# ・subplots / suptitle / tick_params / tier_names / tier_number / tiers_after / tiers_before / tight_layout
# ・to_numpy / upper right / viridis / walk / Walk time / walk_minutes / white / zip
#
# 【選択問題】
# 解答版と同じ結果を再現するために最も重要な確認はどれですか。
# A. 入力値・列名・乱数設定・処理順を問題の指定と一致させる
# B. エラーを読まずに処理を削除する
# C. 毎回異なる変数名と単位へ変更する
# 自分の答え：
#
# 【導出確認】
# 1. 各TODOで作る変数・関数が、次のTODOでどのように使われるか説明してください。
# 2. 最終的な表示・表・グラフ・評価値が何を意味するか説明してください。
# 3. 解答版と比較し、入力、前処理、モデル設定、出力の順に相違点を確認してください。
#
# 【考察問題】
# この結果を実務で利用するときのデータ品質、前提条件、判断上の限界を1つ以上書いてください。
# === 解答対応ガイドここまで ===
