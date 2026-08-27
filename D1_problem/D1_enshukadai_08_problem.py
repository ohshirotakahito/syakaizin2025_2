# -*- coding: utf-8 -*-
"""
D1 演習課題8（問題版）：観光地域を分析して施策を提案しよう
====================================================

広域観光組織の担当者として、40地域の6指標をPCAで要約し、k-meansで
分類して、各グループへ適した観光施策を提案してください。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# データ生成部分は完成済みです。
rng = np.random.default_rng(42)
profiles = np.array([
    [185, 22000, 1.4, 42, 0.22, 4.0],
    [95, 32000, 3.8, 24, 0.30, 4.5],
    [72, 18000, 2.1, 12, 0.82, 4.2],
    [38, 14500, 1.7, 7, 0.38, 4.4],
])
noise_scales = np.array([12, 1800, 0.25, 3.5, 0.05, 0.12])
generated_data = np.vstack([
    rng.normal(profile, noise_scales, size=(10, 6)) for profile in profiles
])
tourism = pd.DataFrame(generated_data, columns=[
    "annual_visitors_10k", "spend_per_person_yen", "average_nights",
    "foreign_visitor_percent", "seasonality_index", "satisfaction_5",
])
tourism.insert(0, "region", [f"Tourism-{n:02d}" for n in range(1, 41)])


# 問題1：データの先頭5行と、各指標の平均・標準偏差を表示します。
# TODO：


# 【選択問題1】seasonality_indexが大きい地域はどのような地域ですか。
# A. 季節による訪問者数の変動が大きい
# B. 必ず満足度が低い
# C. 外国人観光客がいない
# D. 宿泊施設が存在しない
# 答え：


# 問題2：regionを除く6指標を取り出し、StandardScalerで標準化します。
# TODO：


# 【選択問題2】標準化する理由はどれですか。
# A. 円、泊、割合など異なる尺度を公平に扱うため
# B. 地域数を増やすため
# C. 地域名を翻訳するため
# D. 正解ラベルを作るため
# 答え：


# 問題3：PCAで6指標をPC1とPC2へ要約し、各寄与率と累積寄与率を
# 表示してください。
# TODO：


# 【選択問題3】PCAを使う主な目的はどれですか。
# A. 多数の指標を情報を保ちながら少数の軸へ要約する
# B. 地域を正解・不正解に分ける
# C. 欠損値を必ず0にする
# D. 観光客数を将来予測する
# 答え：


# 問題4：k=2〜6でk-meansを行い、各シルエット係数を計算します。
# 最大の係数となるbest_kを求めてください。
# TODO：


# 問題5：best_kで最終モデルを学習し、クラスタ中心を元の単位へ
# 戻して表にしてください。
# TODO：


# 【選択問題4】クラスタ中心を元の単位へ戻す理由はどれですか。
# A. 平均消費額や宿泊数として人が解釈しやすくするため
# B. クラスタ数を増やすため
# C. PCAを取り消すため
# D. 地域名を削除するため
# 答え：


# 問題6：クラスタ中心を読み、次の4つの地域像を割り当てます。
# ・Urban Gateway：訪問者と外国人比率が高い都市型
# ・Stay Resort：宿泊数と消費額が高い滞在型
# ・Seasonal Nature：季節変動が大きい自然観光型
# ・Local Discovery：規模は小さいが地域の魅力を発掘できる型
# TODO：クラスタ番号と地域像の対応を辞書にしてください。


# 問題7：左にクラスタ数とシルエット係数、右にPCA上で色分けした
# 地域セグメントを表示してください。地域名と凡例も追加します。
# TODO：


# 【考察問題】
# 1. 4つの地域像へ、それぞれどのような施策を提案しますか。
# 答え：

# 2. 訪問者数の多い地域を、単純に「優れた地域」と判断できますか。
#    住民生活や環境への影響も含めて考えてください。
# 答え：

# 3. 今回の6指標以外に追加したいデータを2つ以上挙げてください。
# 答え：

# 4. データ分析結果と現地関係者の意見が異なった場合、どのように
#    意思決定するとよいでしょうか。
# 答え：

# === 解答対応ガイド（自動照合済み） ===
#
# 【このガイドの目的】
# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、
# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。
#
# 【解答版に含まれる背景・ヒント】
# ・4種類の観光地域について、6指標の代表値を設定します。
# ・順番：年間訪問者、消費額、宿泊数、外国人比率、季節変動、満足度
# ・都市ゲートウェイ
# ・滞在型リゾート
# ・季節型自然観光
# ・地域発見型
# ・各タイプ10地域、合計40地域を代表値の周辺に生成します。
# ・値を現実的な表示桁へ丸めます。
# ・地域名を除いた6つの数値指標を標準化します。
# ・まずPCAで6次元から2次元へ要約します。
# ・2〜6クラスタを比較し、シルエット係数最大のkを採用します。
# ・選択したkで最終的なクラスタリングを行います。
# ・クラスタ中心を元の単位へ戻し、各グループを解釈します。
# ・番号には意味がないため、中心値の特徴から実務的な名前を付けます。
# ・左にkの評価、右にPCA上の地域セグメントを表示します。
#
# 【実装課題：解答版との対応順】
# TODO 01：必要なライブラリまたは機能 matplotlib.pyplot（別名 plt） を読み込んでください。
# TODO 02：必要なライブラリまたは機能 numpy（別名 np） を読み込んでください。
# TODO 03：必要なライブラリまたは機能 pandas（別名 pd） を読み込んでください。
# TODO 04：必要なライブラリまたは機能 sklearn.cluster.KMeans を読み込んでください。
# TODO 05：必要なライブラリまたは機能 sklearn.decomposition.PCA を読み込んでください。
# TODO 06：必要なライブラリまたは機能 sklearn.metrics.silhouette_score を読み込んでください。
# TODO 07：必要なライブラリまたは機能 sklearn.preprocessing.StandardScaler を読み込んでください。
# TODO 08：rng を作成・更新してください。 使用する処理：np.random.default_rng。 主な指定値：42。
# TODO 09：profiles を作成・更新してください。 使用する処理：np.array。 主な指定値：185, 22000, 1.4, 42, 0.22, 4.0, 95, 32000, 3.8, 24, 0.3, 4.5。
# TODO 10：noise_scales を作成・更新してください。 使用する処理：np.array。 主な指定値：12, 1800, 0.25, 3.5, 0.05, 0.12。
# TODO 11：generated_rows を作成・更新してください。
# TODO 12：profiles を順に処理する反復を作ってください。 使用する処理：generated_rows.append, rng.normal。 主な指定値：10, 6。
# TODO 13：generated_data を作成・更新してください。 使用する処理：np.vstack。
# TODO 14：tourism を作成・更新してください。 使用する処理：pd.DataFrame。 主な指定値：'annual_visitors_10k', 'spend_per_person_yen', 'average_nights', 'foreign_visitor_percent', 'seasonality_index', 'satisfaction_5'。
# TODO 15：次の処理を実行してください。 使用する処理：tourism.insert, range。 主な指定値：0, 'region', 'Tourism-', 1, 41, '02d'。
# TODO 16：指定された変数 を作成・更新してください。 使用する処理：round。 主な指定値：'annual_visitors_10k', 1。
# TODO 17：指定された変数 を作成・更新してください。 使用する処理：astype, round。 主な指定値：'spend_per_person_yen'。
# TODO 18：指定された変数 を作成・更新してください。 使用する処理：round。 主な指定値：'average_nights', 2。
# TODO 19：指定された変数 を作成・更新してください。 使用する処理：round。 主な指定値：'foreign_visitor_percent', 1。
# TODO 20：指定された変数 を作成・更新してください。 使用する処理：round, clip。 主な指定値：'seasonality_index', 2, 0, 1。
# TODO 21：指定された変数 を作成・更新してください。 使用する処理：round, clip。 主な指定値：'satisfaction_5', 2, 1, 5。
# TODO 22：次の処理を実行してください。 使用する処理：print。 主な指定値：'【観光地域データ】'。
# TODO 23：次の処理を実行してください。 使用する処理：print, tourism.head。
# TODO 24：feature_names を作成・更新してください。 使用する処理：tourism.columns.drop。 主な指定値：'region'。
# TODO 25：features を作成・更新してください。
# TODO 26：scaler を作成・更新してください。 使用する処理：StandardScaler。
# TODO 27：scaled_features を作成・更新してください。 使用する処理：scaler.fit_transform。
# TODO 28：pca を作成・更新してください。 使用する処理：PCA。 主な指定値：2。
# TODO 29：points を作成・更新してください。 使用する処理：pca.fit_transform。
# TODO 30：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【PCAの寄与率】'。
# TODO 31：次の処理を実行してください。 使用する処理：print。 主な指定値：'PC1: ', 0, '.1%'。
# TODO 32：次の処理を実行してください。 使用する処理：print。 主な指定値：'PC2: ', 1, '.1%'。
# TODO 33：次の処理を実行してください。 使用する処理：print, pca.explained_variance_ratio_.sum。 主な指定値：'累積: ', '.1%'。
# TODO 34：k_candidates を作成・更新してください。 使用する処理：range。 主な指定値：2, 7。
# TODO 35：scores を作成・更新してください。
# TODO 36：k_candidates を順に処理する反復を作ってください。 使用する処理：KMeans, candidate.fit_predict, silhouette_score, scores.append, print。 主な指定値：42, 10, 'k=', ': シルエット係数=', '.3f'。
# TODO 37：best_k を作成・更新してください。 使用する処理：list, int, np.argmax。
# TODO 38：次の処理を実行してください。 使用する処理：print。 主な指定値：'採用クラスタ数: '。
# TODO 39：model を作成・更新してください。 使用する処理：KMeans。 主な指定値：42, 10。
# TODO 40：clusters を作成・更新してください。 使用する処理：model.fit_predict。
# TODO 41：centers を作成・更新してください。 使用する処理：pd.DataFrame, scaler.inverse_transform。
# TODO 42：urban を作成・更新してください。 使用する処理：idxmax。 主な指定値：'annual_visitors_10k'。
# TODO 43：remaining を作成・更新してください。 使用する処理：centers.drop。
# TODO 44：resort を作成・更新してください。 使用する処理：idxmax。 主な指定値：'average_nights'。
# TODO 45：remaining を作成・更新してください。 使用する処理：remaining.drop。
# TODO 46：seasonal を作成・更新してください。 使用する処理：idxmax。 主な指定値：'seasonality_index'。
# TODO 47：local を作成・更新してください。 使用する処理：remaining.drop。 主な指定値：0。
# TODO 48：segment_names を作成・更新してください。 主な指定値：'Urban Gateway', 'Stay Resort', 'Seasonal Nature', 'Local Discovery'。
# TODO 49：指定された変数 を作成・更新してください。 主な指定値：'cluster'。
# TODO 50：指定された変数 を作成・更新してください。 使用する処理：map。 主な指定値：'segment', 'cluster'。
# TODO 51：指定された変数 を作成・更新してください。 使用する処理：centers.index.map。 主な指定値：'segment'。
# TODO 52：指定された変数 を作成・更新してください。 使用する処理：to_numpy, sort_index, value_counts, pd.Series。 主な指定値：'regions'。
# TODO 53：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【セグメント別の平均像】'。
# TODO 54：次の処理を実行してください。 使用する処理：print, round, centers.set_index。 主な指定値：2, 'segment'。
# TODO 55：strategies を作成・更新してください。 主な指定値：'Urban Gateway', 'Stay Resort', 'Seasonal Nature', 'Local Discovery', '混雑分散、地方周遊への送客、多言語案内', '連泊商品、高付加価値体験、リピーター施策', '閑散期イベント、通年コンテンツ、予約平準化', '認知向上、交通案内、地域文化の物語化'。
# TODO 56：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【推奨施策】'。
# TODO 57：strategies.items() を順に処理する反復を作ってください。 使用する処理：strategies.items, print。 主な指定値：': ', '16s'。
# TODO 58：fig, axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, 14, 5.5。
# TODO 59：次の処理を実行してください。 使用する処理：plot, list。 主な指定値：'o', '#4C78A8', 0。
# TODO 60：次の処理を実行してください。 使用する処理：axvline。 主な指定値：'#E45756', '--', 0, 'Selected k='。
# TODO 61：次の処理を実行してください。 使用する処理：set_xlabel。 主な指定値：'Number of clusters', 0。
# TODO 62：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Silhouette score', 0。
# TODO 63：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Cluster Number Selection', 0。
# TODO 64：次の処理を実行してください。 使用する処理：set_xticks, list。 主な指定値：0。
# TODO 65：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 0。
# TODO 66：次の処理を実行してください。 使用する処理：legend。 主な指定値：0。
# TODO 67：colors を作成・更新してください。 主な指定値：'Urban Gateway', 'Stay Resort', 'Seasonal Nature', 'Local Discovery', '#4C78A8', '#E45756', '#F2CF5B', '#54A24B'。
# TODO 68：colors.items() を順に処理する反復を作ってください。 使用する処理：colors.items, scatter。 主な指定値：'segment', 75, 0.85, 1, 0。
# TODO 69：enumerate(tourism['region']) を順に処理する反復を作ってください。 使用する処理：enumerate, annotate。 主な指定値：'region', 'offset points', 6.5, 1, 3。
# TODO 70：次の処理を実行してください。 使用する処理：set_xlabel。 主な指定値：'PC1 (', ')', 1, 0, '.1%'。
# TODO 71：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'PC2 (', ')', 1, '.1%'。
# TODO 72：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Tourism Region Segments', 1。
# TODO 73：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 1。
# TODO 74：次の処理を実行してください。 使用する処理：legend。 主な指定値：8, 1。
# TODO 75：次の処理を実行してください。 使用する処理：fig.tight_layout。
# TODO 76：次の処理を実行してください。 使用する処理：plt.show。
# TODO 77：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【注意】'。
# TODO 78：次の処理を実行してください。 使用する処理：print。 主な指定値：'分類は施策検討の出発点です。同じグループでも地域文化や住民の意向は'。
# TODO 79：次の処理を実行してください。 使用する処理：print。 主な指定値：'異なるため、現地調査と対話を組み合わせて最終判断します。'。
#
# 【使用する名前・データ仕様】
# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。
# ・annotate / annual_visitors_10k / append / argmax / array / astype / average_nights / axes
# ・axvline / best_k / candidate / centers / clip / cluster / Cluster Number Selection / clusters
# ・color / colors / DataFrame / default_rng / drop / enumerate / feature_names / features
# ・fit_predict / fit_transform / foreign_visitor_percent / generated_data / generated_rows / grid / head / idxmax
# ・insert / inverse_transform / items / k_candidates / KMeans / labels / legend / local
# ・Local Discovery / map / noise_scales / normal / Number of clusters / offset points / pca / PCA
# ・plot / points / profile / profiles / region / regions / remaining / resort
# ・rng / round / satisfaction_5 / scaled_features / scaler / scatter / score / scores
# ・seasonal / Seasonal Nature / seasonality_index / segment / segment_names / selected / Series / set_index
# ・set_title / set_xlabel / set_xticks / set_ylabel / show / Silhouette score / silhouette_score / sort_index
# ・spend_per_person_yen / StandardScaler / Stay Resort / strategies / strategy / subplots / sum / tight_layout
# ・to_numpy / tourism / Tourism Region Segments / Tourism- / urban / Urban Gateway / value_counts / vstack
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
