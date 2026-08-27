# -*- coding: utf-8 -*-
"""
D1 演習課題4（問題版）：購買履歴から顧客施策を考えよう
====================================================

【あなたの役割】
あなたはECサイトのCRM担当者です。購買行動の似た顧客をk-meansで分類し、
各グループに適した販売促進策を提案してください。

TODOへコードを書き、選択問題と考察問題にも答えてください。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# 顧客データは完成済みです。変更せずに使用してください。
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


# ==================================================================
# 問題1：機械学習へ渡す特徴量を準備する
# ==================================================================
# TODO 1-A：customersの先頭5行を表示してください。


# TODO 1-B：annual_orders、avg_order_yen、days_since_lastの3列を
# featuresへ代入してください。customer_idは含めません。


# 【選択問題1】
# customer_idをk-meansへ渡さない理由はどれですか。
#
# A. IDは顧客の購買行動を表す量的な特徴ではないから
# B. IDは必ず欠損しているから
# C. k-meansでは列を3つまでしか使えないから
# D. 顧客数が少なくなるから
#
# 自分の答え：


# ==================================================================
# 問題2：特徴量を標準化する
# ==================================================================
# TODO 2-A：StandardScalerを作り、scalerへ代入してください。


# TODO 2-B：featuresを標準化し、scaled_featuresへ代入してください。


# 【選択問題2】
# 標準化せずにk-meansを実行すると、どの項目が特に強く影響しそうですか。
#
# A. 年間注文回数
# B. 平均注文額
# C. 最終購入からの日数
# D. 顧客ID
#
# 自分の答え：
# 理由：


# ==================================================================
# 問題3：適切なクラスタ数を検討する
# ==================================================================
# TODO 3-A：クラスタ数2から6までを順番に試してください。
# 各kについてKMeansを学習し、シルエット係数を計算して、
# silhouette_scoresへ追加してください。
#
# 設定：random_state=42、n_init=10


# TODO 3-B：シルエット係数が最大になるbest_kを求めてください。
# ヒント：np.argmax()を使用できます。


# 【選択問題3】
# シルエット係数について、正しい説明はどれですか。
#
# A. 大きいほど、同じクラスタ内がまとまり、別クラスタと離れている
# B. 小さいほど、分類の正解率が高い
# C. 必ずクラスタ数と同じ値になる
# D. 顧客の平均注文額を表す
#
# 自分の答え：


# ==================================================================
# 問題4：最終的なk-meansモデルを作る
# ==================================================================
# TODO 4-A：best_kを使ってKMeansを学習し、各顧客のクラスタ番号を
# cluster_numbersへ代入してください。


# TODO 4-B：model.cluster_centers_をinverse_transform()で元の単位へ
# 戻し、centers_originalへ代入してください。


# TODO 4-C：クラスタごとの注文回数、注文額、最終購入日数の平均を
# 表として表示してください。


# 【選択問題4】
# クラスタ番号0、1、2、3について正しい説明はどれですか。
#
# A. 0が最も価値の低い顧客を意味する
# B. 数字が大きいほど重要な顧客を意味する
# C. 番号は識別用で、順序や良し悪しの意味はない
# D. すべての実行で必ず同じ顧客像を表す
#
# 自分の答え：


# ==================================================================
# 問題5：クラスタへ顧客像の名前を付ける
# ==================================================================
# 各クラスタ中心を確認し、次の顧客像を1つずつ割り当ててください。
#
# Loyal VIP             : 最近も購入し、平均注文額が高い
# Frequent / Value      : 注文回数が多く、1回の注文額はお手頃
# Dormant / Win-back    : 最終購入から長期間経過している
# Developing            : 注文が少なく、今後の育成余地がある
#
# TODO 5-A：クラスタ番号と顧客像の対応を辞書persona_by_clusterで作ります。


# TODO 5-B：customersへcluster列とpersona列を追加してください。


# 【考察問題1】
# 各顧客像に、どのようなクーポンや案内を送るとよいでしょうか。
# Loyal VIP：
# Frequent / Value：
# Dormant / Win-back：
# Developing：


# ==================================================================
# 問題6：分析結果を可視化する
# ==================================================================
# TODO 6-A：横軸をクラスタ数、縦軸をシルエット係数とする折れ線グラフを
# 作成してください。採用したbest_kの位置も示してください。


# TODO 6-B：PCAを使い、標準化した3項目を2次元へ変換してください。


# TODO 6-C：横軸をPCA第1成分、縦軸を第2成分として、顧客像ごとに
# 色分けした散布図を作ってください。顧客IDと凡例も表示します。


# ==================================================================
# 最終考察
# ==================================================================
# 1. 今回の顧客分類を、売上向上のためにどのように利用できますか。
# 自分の答え：


# 2. 分析に追加すると、よりよい顧客分類ができそうな情報を2つ以上
# 挙げてください。
# 自分の答え：


# 3. このクラスタだけで顧客の価値を決めることには、どのような危険が
# ありますか。
# 自分の答え：

# === 解答対応ガイド（自動照合済み） ===
#
# 【このガイドの目的】
# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、
# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。
#
# 【解答版に含まれる背景・ヒント】
# ・グラフ描画に使用します。
# ・数値計算に使用します。
# ・表形式のデータ作成と集計に使用します。
# ・k-meansによるクラスタリングに使用します。
# ・多次元の顧客データを2次元グラフへ要約するために使用します。
# ・クラスタのまとまり具合を評価するシルエット係数を計算します。
# ・単位の異なる3項目を公平に比較できるよう標準化します。
# ・32人の架空顧客について、過去1年間の購買履歴を用意します。
# ・annual_orders    : 過去1年間の注文回数
# ・avg_order_yen    : 1回あたり平均注文額（円）
# ・days_since_last  : 最終購入からの経過日数（日、小さいほど最近購入）
# ・customer_idは識別用の文字列なので、機械学習へは渡しません。
# ・3つの数値列だけをfeaturesへ取り出します。
# ・注文額は数万円、注文回数は数十回なので、単位と桁が異なります。
# ・StandardScalerで、各列を平均0・標準偏差1の尺度へ変換します。
# ・適切なクラスタ数を考えるため、2から6クラスタまで試します。
# ・シルエット係数は-1から1の範囲で、大きいほどクラスタ内がまとまり、
# ・異なるクラスタ同士が離れていることを表します。
# ・比較するすべてのkで同じ条件になるよう設定します。
# ・各顧客をクラスタへ割り当てます。
# ・標準化空間でのシルエット係数を計算し、リストへ追加します。
# ・np.argmax()は最大値がある位置を返します。
# ・その位置をcandidate_kへ対応させ、最も評価の高いクラスタ数を選びます。
# ・選んだクラスタ数で最終モデルを学習します。
# ・標準化されたクラスタ中心を、inverse_transform()で円・回・日の
# ・元の単位へ戻します。これにより各クラスタの顧客像を解釈できます。
# ・value_counts()で各クラスタの人数を数え、クラスタ番号順に追加します。
# ・k-meansの番号は無作為なので、中心値を使って実務向けの名前を付けます。
# ・最終購入からの日数が最も長いクラスタを「休眠・離反注意」とします。
# ・休眠クラスタを除き、平均注文額が最も高いものを「優良VIP」とします。
# ・残った中で注文回数が最も多いものを「頻繁・お手頃」とします。
# ・最後に残ったクラスタを「育成候補」とします。
# ・各顧客へクラスタ番号と顧客像の名前を追加します。
# ・顧客像ごとに考えられる施策例を用意します。
# ・1つ目のグラフ：クラスタ数とシルエット係数の関係を描きます。
# ・3項目のデータをPCAで2次元へ要約し、散布図で見えるようにします。
# ・顧客像ごとに色を固定し、凡例を分かりやすくします。
# ・各点へ顧客IDを表示し、元データと照合できるようにします。
#
# 【実装課題：解答版との対応順】
# TODO 01：必要なライブラリまたは機能 matplotlib.pyplot（別名 plt） を読み込んでください。
# TODO 02：必要なライブラリまたは機能 numpy（別名 np） を読み込んでください。
# TODO 03：必要なライブラリまたは機能 pandas（別名 pd） を読み込んでください。
# TODO 04：必要なライブラリまたは機能 sklearn.cluster.KMeans を読み込んでください。
# TODO 05：必要なライブラリまたは機能 sklearn.decomposition.PCA を読み込んでください。
# TODO 06：必要なライブラリまたは機能 sklearn.metrics.silhouette_score を読み込んでください。
# TODO 07：必要なライブラリまたは機能 sklearn.preprocessing.StandardScaler を読み込んでください。
# TODO 08：customers, number を作成・更新してください。 使用する処理：pd.DataFrame, range。 主な指定値：'customer_id', 'annual_orders', 'avg_order_yen', 'days_since_last', 24, 28, 21, 30, 19, 26, 23, 27。
# TODO 09：次の処理を実行してください。 使用する処理：print。 主な指定値：'【顧客データ：先頭5行】'。
# TODO 10：次の処理を実行してください。 使用する処理：print, customers.head。
# TODO 11：feature_names を作成・更新してください。 主な指定値：'annual_orders', 'avg_order_yen', 'days_since_last'。
# TODO 12：features を作成・更新してください。
# TODO 13：scaler を作成・更新してください。 使用する処理：StandardScaler。
# TODO 14：scaled_features を作成・更新してください。 使用する処理：scaler.fit_transform。
# TODO 15：candidate_k を作成・更新してください。 使用する処理：range。 主な指定値：2, 7。
# TODO 16：silhouette_scores を作成・更新してください。
# TODO 17：candidate_k を順に処理する反復を作ってください。 使用する処理：KMeans, candidate_model.fit_predict, silhouette_score, silhouette_scores.append, print。 主な指定値：42, 10, 'クラスタ数=', ': シルエット係数=', '.3f'。
# TODO 18：best_k を作成・更新してください。 使用する処理：list, int, np.argmax。
# TODO 19：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n採用するクラスタ数: '。
# TODO 20：model を作成・更新してください。 使用する処理：KMeans。 主な指定値：42, 10。
# TODO 21：cluster_numbers を作成・更新してください。 使用する処理：model.fit_predict。
# TODO 22：centers_original を作成・更新してください。 使用する処理：scaler.inverse_transform。
# TODO 23：cluster_summary を作成・更新してください。 使用する処理：pd.DataFrame。
# TODO 24：指定された変数 を作成・更新してください。 使用する処理：to_numpy, sort_index, value_counts, pd.Series。 主な指定値：'customers'。
# TODO 25：dormant_cluster を作成・更新してください。 使用する処理：idxmax。 主な指定値：'days_since_last'。
# TODO 26：remaining を作成・更新してください。 使用する処理：cluster_summary.drop。
# TODO 27：vip_cluster を作成・更新してください。 使用する処理：idxmax。 主な指定値：'avg_order_yen'。
# TODO 28：remaining を作成・更新してください。 使用する処理：remaining.drop。
# TODO 29：frequent_cluster を作成・更新してください。 使用する処理：idxmax。 主な指定値：'annual_orders'。
# TODO 30：developing_cluster を作成・更新してください。 使用する処理：remaining.drop。 主な指定値：0。
# TODO 31：persona_by_cluster を作成・更新してください。 主な指定値：'Dormant / Win-back', 'Loyal VIP', 'Frequent / Value', 'Developing'。
# TODO 32：指定された変数 を作成・更新してください。 主な指定値：'cluster'。
# TODO 33：指定された変数 を作成・更新してください。 使用する処理：map。 主な指定値：'persona', 'cluster'。
# TODO 34：指定された変数 を作成・更新してください。 使用する処理：cluster_summary.index.map。 主な指定値：'persona'。
# TODO 35：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【クラスタごとの平均的な顧客像】'。
# TODO 36：次の処理を実行してください。 使用する処理：print, round, cluster_summary.set_index。 主な指定値：1, 'persona'。
# TODO 37：actions を作成・更新してください。 主な指定値：'Loyal VIP', 'Frequent / Value', 'Dormant / Win-back', 'Developing', '先行販売、限定商品、VIP会員特典', 'まとめ買い割引、送料無料条件の提案', '再購入クーポン、離反理由アンケート', '初回購入後のフォロー、関連商品の紹介'。
# TODO 38：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【顧客像ごとの施策例】'。
# TODO 39：actions.items() を順に処理する反復を作ってください。 使用する処理：actions.items, sum, print。 主な指定値：' (', '人): ', 'persona', '22s'。
# TODO 40：fig, axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, 13, 5。
# TODO 41：次の処理を実行してください。 使用する処理：plot, list。 主な指定値：'o', '#4C78A8', 0。
# TODO 42：次の処理を実行してください。 使用する処理：axvline。 主な指定値：'#E45756', '--', 0, 'Selected k = '。
# TODO 43：次の処理を実行してください。 使用する処理：set_xlabel。 主な指定値：'Number of clusters (k)', 0。
# TODO 44：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Silhouette score', 0。
# TODO 45：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Selecting the Number of Customer Segments', 0。
# TODO 46：次の処理を実行してください。 使用する処理：set_xticks, list。 主な指定値：0。
# TODO 47：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 0。
# TODO 48：次の処理を実行してください。 使用する処理：legend。 主な指定値：0。
# TODO 49：pca を作成・更新してください。 使用する処理：PCA。 主な指定値：2。
# TODO 50：points_2d を作成・更新してください。 使用する処理：pca.fit_transform。
# TODO 51：persona_colors を作成・更新してください。 主な指定値：'Loyal VIP', 'Frequent / Value', 'Dormant / Win-back', 'Developing', '#E45756', '#4C78A8', '#B279A2', '#54A24B'。
# TODO 52：persona_colors.items() を順に処理する反復を作ってください。 使用する処理：persona_colors.items, scatter。 主な指定値：'persona', 75, 0.85, 1, 0。
# TODO 53：enumerate(customers['customer_id']) を順に処理する反復を作ってください。 使用する処理：enumerate, annotate。 主な指定値：'customer_id', 'offset points', 7, 1, 4, 3。
# TODO 54：次の処理を実行してください。 使用する処理：set_xlabel。 主な指定値：'PCA component 1', 1。
# TODO 55：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'PCA component 2', 1。
# TODO 56：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Customer Segments', 1。
# TODO 57：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 1。
# TODO 58：次の処理を実行してください。 使用する処理：legend。 主な指定値：'Recommended action group', 8, 1。
# TODO 59：次の処理を実行してください。 使用する処理：fig.tight_layout。
# TODO 60：次の処理を実行してください。 使用する処理：plt.show。
# TODO 61：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【注意】'。
# TODO 62：次の処理を実行してください。 使用する処理：print。 主な指定値：'クラスタは施策を考える手掛かりであり、顧客の価値を決めるものではありません。'。
# TODO 63：次の処理を実行してください。 使用する処理：print。 主な指定値：'実務では定期的に再学習し、施策後の反応も検証する必要があります。'。
#
# 【使用する名前・データ仕様】
# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。
# ・action / actions / annotate / annual_orders / append / argmax / avg_order_yen / axes
# ・axvline / best_k / candidate_k / candidate_labels / candidate_model / centers_original / cluster / cluster_numbers
# ・cluster_summary / color / count / Customer Segments / customer_id / customers / DataFrame / days_since_last
# ・Developing / developing_cluster / Dormant / Win-back / dormant_cluster / drop / enumerate / feature_names / features
# ・fit_predict / fit_transform / Frequent / Value / frequent_cluster / grid / head / idxmax / inverse_transform
# ・items / KMeans / legend / Loyal VIP / map / number / offset points / pca
# ・PCA / PCA component 1 / PCA component 2 / persona / persona_by_cluster / persona_colors / plot / points_2d
# ・Recommended action group / remaining / round / scaled_features / scaler / scatter / score / selected
# ・Selecting the Number of Customer Segments / Series / set_index / set_title / set_xlabel / set_xticks / set_ylabel / show
# ・Silhouette score / silhouette_score / silhouette_scores / sort_index / StandardScaler / subplots / sum / tight_layout
# ・to_numpy / value_counts / vip_cluster
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
