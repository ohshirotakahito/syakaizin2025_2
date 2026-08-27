# -*- coding: utf-8 -*-
"""
D1 演習課題6（問題版）：フードデリバリーの所要時間を予測しよう
==========================================================

【あなたの役割】
あなたはフードデリバリー会社のデータ分析担当者です。注文時の情報から
配達完了までの時間を予測し、お客様へ現実的な到着予定を案内してください。

TODOへコードを書き、選択問題と考察問題にも答えてください。
データは演習用に生成した架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# 架空データの生成部分は完成済みです。変更せずに使用してください。
rng = np.random.default_rng(42)
number_of_orders = 600
distance_km = rng.uniform(0.5, 12.0, number_of_orders)
item_count = rng.integers(1, 9, number_of_orders)
restaurant_prep_minutes = np.clip(rng.normal(16, 5, number_of_orders), 5, 35)
traffic_level = rng.integers(1, 4, number_of_orders)
is_raining = rng.binomial(1, 0.25, number_of_orders)
courier_active_orders = rng.integers(1, 5, number_of_orders)
noise = rng.normal(0, 4.5, number_of_orders)

delivery_minutes = (
    5
    + 3.2 * distance_km
    + 0.9 * item_count
    + 0.75 * restaurant_prep_minutes
    + 4.5 * (traffic_level - 1)
    + 6.0 * is_raining
    + 2.8 * (courier_active_orders - 1)
    + noise
)

deliveries = pd.DataFrame({
    "distance_km": distance_km.round(2),
    "item_count": item_count,
    "restaurant_prep_minutes": restaurant_prep_minutes.round(1),
    "traffic_level": traffic_level,
    "is_raining": is_raining,
    "courier_active_orders": courier_active_orders,
    "delivery_minutes": delivery_minutes.round(1),
})


# ==================================================================
# 問題1：説明変数と目的変数を準備する
# ==================================================================
# TODO 1-A：deliveriesの先頭5行、注文数、平均配達時間を表示してください。


# TODO 1-B：delivery_minutes以外の列をXへ、delivery_minutesをyへ
# 代入してください。


# 【選択問題1】
# 今回の分析が「回帰」である理由はどれですか。
#
# A. 配達する・しないの2分類を予測するから
# B. 配達時間という連続した数値を予測するから
# C. 注文を3グループに分けるから
# D. 正解ラベルを使わないから
#
# 自分の答え：


# ==================================================================
# 問題2：学習用とテスト用へ分割する
# ==================================================================
# TODO 2-A：Xとyを学習用75%、テスト用25%へ分割してください。
# random_state=42を指定します。


# 【選択問題2】
# 回帰の分割でstratifyを通常指定しない理由として適切なものはどれですか。
#
# A. 目的変数が連続値で、分類クラスではないから
# B. テストデータが不要だから
# C. 説明変数が6個あるから
# D. LinearRegressionでは乱数を使えないから
#
# 自分の答え：


# ==================================================================
# 問題3：線形回帰モデルを学習する
# ==================================================================
# TODO 3-A：LinearRegressionのモデルを作り、modelへ代入してください。


# TODO 3-B：X_trainとy_trainを使ってモデルを学習してください。


# TODO 3-C：X_testの配達時間を予測し、predictedへ代入してください。


# ==================================================================
# 問題4：予測性能を評価する
# ==================================================================
# TODO 4-A：MAE、RMSE、R2を計算して表示してください。
# RMSEはmean_squared_errorの平方根で求められます。


# 【選択問題3】
# MAEが4.0分だった場合の解釈として正しいものはどれですか。
#
# A. すべての予測が必ず4分遅い
# B. 予測は実際の時間から平均して約4分ずれている
# C. 4%の注文だけ正しく予測できた
# D. 配達時間の平均が4分である
#
# 自分の答え：


# 【選択問題4】
# R2が1に近い場合、何を意味しますか。
#
# A. モデルが配達時間のばらつきをよく説明できている
# B. すべての係数が1である
# C. 説明変数が1個しかない
# D. 予測誤差が必ず1分である
#
# 自分の答え：


# ==================================================================
# 問題5：回帰係数を解釈する
# ==================================================================
# TODO 5-A：X.columnsとmodel.coef_を使い、項目名と係数の表を作ります。


# TODO 5-B：切片model.intercept_も表示してください。


# 【選択問題5】
# distance_kmの係数が3.2だった場合、どのように解釈しますか。
#
# A. 距離が1km増えると、ほかの条件が同じなら約3.2分長くなる
# B. すべての配達距離が3.2kmである
# C. 配達時間を3.2分以内にできる
# D. 距離が配達時間へ影響していない
#
# 自分の答え：


# ==================================================================
# 問題6：新しい注文を予測する
# ==================================================================
# 次の注文について予想到着時間を計算してください。
# 距離5.5km、商品3点、調理18分、交通量3、雨あり、担当注文2件
#
# TODO 6-A：上記の値を、Xと同じ列名のDataFrameへまとめます。


# TODO 6-B：model.predict()で配達時間を予測して表示してください。


# 【考察問題1】
# お客様には予測値を1つの時刻として断定せず、どのように案内すると
# よいでしょうか。
# 自分の答え：


# ==================================================================
# 問題7：予測結果を可視化する
# ==================================================================
# TODO 7-A：横軸を実際の時間、縦軸を予測時間とする散布図を作ります。
# 完全に予測できた場合を示す対角線も追加してください。


# TODO 7-B：残差「実際の時間 - 予測時間」を計算し、横軸を予測時間、
# 縦軸を残差とする散布図を作ってください。残差0の線も追加します。


# 【選択問題6】
# 良い残差プロットの特徴として最も適切なものはどれですか。
#
# A. 残差が0付近へ規則的な形を作らず散らばっている
# B. すべての残差が右肩上がりに並ぶ
# C. 予測時間が長いほど必ず残差が大きくなる
# D. 残差がすべて正になる
#
# 自分の答え：


# ==================================================================
# 最終考察
# ==================================================================
# 1. 今回使っていない要因で、配達時間へ影響しそうなものを2つ以上
# 挙げてください。
# 自分の答え：


# 2. 予測時間より実際の配達が遅れた注文を、業務改善へどのように
# 活用できますか。
# 自分の答え：


# 3. 線形回帰では表現しにくそうな関係を1つ考えてください。
# 自分の答え：

# === 解答対応ガイド（自動照合済み） ===
#
# 【このガイドの目的】
# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、
# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。
#
# 【解答版に含まれる背景・ヒント】
# ・乱数を固定し、実行するたびに同じデータを生成します。
# ・注文時点で分かる情報を現実的な範囲で生成します。
# ・1=少、2=中、3=多
# ・0=晴れ、1=雨
# ・所要時間を作ります。各要因の影響に加え、現実の予測しきれない揺らぎを
# ・noiseとして加えています。
# ・説明変数と目的変数を1つのDataFrameへまとめます。
# ・Xは予測に使う説明変数、yは予測したい配達時間です。
# ・学習用75%、テスト用25%に分割します。
# ・回帰では目的変数が連続値なので、分類で使ったstratifyは指定しません。
# ・線形回帰モデルを作り、学習用データから関係を学習します。
# ・未使用だったテストデータの配達時間を予測します。
# ・MAEは、予測が実際の値から平均何分ずれたかを表します。
# ・RMSEは大きな予測誤差をMAEより強く評価します。
# ・R2は、配達時間のばらつきをモデルがどの程度説明できたかを表します。
# ・1に近いほどよく説明でき、0なら平均値予測と同程度です。
# ・係数は、ほかの条件が同じとき、その項目が1増えることで予測時間が
# ・何分変化するかを表します。
# ・実際の配達時間と予測時間を比較する表を作ります。
# ・新しい注文の例を作り、到着予定時間を予測します。
# ・左：実測値と予測値、右：予測値と残差を表示します。
# ・残差は「実測値 - 予測値」です。0付近へランダムに散らばるのが理想です。
#
# 【実装課題：解答版との対応順】
# TODO 01：必要なライブラリまたは機能 matplotlib.pyplot（別名 plt） を読み込んでください。
# TODO 02：必要なライブラリまたは機能 numpy（別名 np） を読み込んでください。
# TODO 03：必要なライブラリまたは機能 pandas（別名 pd） を読み込んでください。
# TODO 04：必要なライブラリまたは機能 sklearn.linear_model.LinearRegression を読み込んでください。
# TODO 05：必要なライブラリまたは機能 sklearn.metrics.mean_absolute_error, sklearn.metrics.mean_squared_error, sklearn.metrics.r2_score を読み込んでください。
# TODO 06：必要なライブラリまたは機能 sklearn.model_selection.train_test_split を読み込んでください。
# TODO 07：rng を作成・更新してください。 使用する処理：np.random.default_rng。 主な指定値：42。
# TODO 08：number_of_orders を作成・更新してください。 主な指定値：600。
# TODO 09：distance_km を作成・更新してください。 使用する処理：rng.uniform。 主な指定値：0.5, 12.0。
# TODO 10：item_count を作成・更新してください。 使用する処理：rng.integers。 主な指定値：1, 9。
# TODO 11：restaurant_prep_minutes を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：5, 35, 16。
# TODO 12：traffic_level を作成・更新してください。 使用する処理：rng.integers。 主な指定値：1, 4。
# TODO 13：is_raining を作成・更新してください。 使用する処理：rng.binomial。 主な指定値：1, 0.25。
# TODO 14：courier_active_orders を作成・更新してください。 使用する処理：rng.integers。 主な指定値：1, 5。
# TODO 15：noise を作成・更新してください。 使用する処理：rng.normal。 主な指定値：0, 4.5。
# TODO 16：delivery_minutes を作成・更新してください。 主な指定値：2.8, 6.0, 1, 4.5, 0.75, 5, 0.9, 3.2。
# TODO 17：deliveries を作成・更新してください。 使用する処理：pd.DataFrame, distance_km.round, restaurant_prep_minutes.round, delivery_minutes.round。 主な指定値：'distance_km', 'item_count', 'restaurant_prep_minutes', 'traffic_level', 'is_raining', 'courier_active_orders', 'delivery_minutes', 2, 1。
# TODO 18：次の処理を実行してください。 使用する処理：print。 主な指定値：'【配達データ：先頭5行】'。
# TODO 19：次の処理を実行してください。 使用する処理：print, deliveries.head。
# TODO 20：次の処理を実行してください。 使用する処理：print, len。 主な指定値：'\n注文数: ', '件'。
# TODO 21：次の処理を実行してください。 使用する処理：print, mean。 主な指定値：'平均配達時間: ', '分', '.1f', 'delivery_minutes'。
# TODO 22：X を作成・更新してください。 使用する処理：deliveries.drop。 主な指定値：'delivery_minutes'。
# TODO 23：y を作成・更新してください。 主な指定値：'delivery_minutes'。
# TODO 24：X_train, X_test, y_train, y_test を作成・更新してください。 使用する処理：train_test_split。 主な指定値：0.25, 42。
# TODO 25：model を作成・更新してください。 使用する処理：LinearRegression。
# TODO 26：次の処理を実行してください。 使用する処理：model.fit。
# TODO 27：predicted を作成・更新してください。 使用する処理：model.predict。
# TODO 28：mae を作成・更新してください。 使用する処理：mean_absolute_error。
# TODO 29：rmse を作成・更新してください。 使用する処理：np.sqrt, mean_squared_error。
# TODO 30：r2 を作成・更新してください。 使用する処理：r2_score。
# TODO 31：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【モデル評価】'。
# TODO 32：次の処理を実行してください。 使用する処理：print。 主な指定値：'平均絶対誤差（MAE）: ', '分', '.2f'。
# TODO 33：次の処理を実行してください。 使用する処理：print。 主な指定値：'二乗平均平方根誤差（RMSE）: ', '分', '.2f'。
# TODO 34：次の処理を実行してください。 使用する処理：print。 主な指定値：'決定係数（R2）: ', '.3f'。
# TODO 35：coefficient_table を作成・更新してください。 使用する処理：sort_values, pd.DataFrame。 主な指定値：'coefficient_minutes', False, 'feature'。
# TODO 36：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【各項目の回帰係数】'。
# TODO 37：次の処理を実行してください。 使用する処理：print, to_string, coefficient_table.round。 主な指定値：False, 3。
# TODO 38：次の処理を実行してください。 使用する処理：print。 主な指定値：'切片: ', '分', '.3f'。
# TODO 39：results を作成・更新してください。 使用する処理：X_test.copy。
# TODO 40：指定された変数 を作成・更新してください。 主な指定値：'actual_minutes'。
# TODO 41：指定された変数 を作成・更新してください。 主な指定値：'predicted_minutes'。
# TODO 42：指定された変数 を作成・更新してください。 主な指定値：'error_minutes'。
# TODO 43：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【予測結果：先頭10件】'。
# TODO 44：次の処理を実行してください。 使用する処理：print, round, results.head。 主な指定値：1, 10。
# TODO 45：new_order を作成・更新してください。 使用する処理：pd.DataFrame。 主な指定値：'distance_km', 'item_count', 'restaurant_prep_minutes', 'traffic_level', 'is_raining', 'courier_active_orders', 5.5, 3, 18.0, 1, 2。
# TODO 46：new_prediction を作成・更新してください。 使用する処理：model.predict。 主な指定値：0。
# TODO 47：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【新しい注文の予測】'。
# TODO 48：次の処理を実行してください。 使用する処理：print。
# TODO 49：次の処理を実行してください。 使用する処理：print。 主な指定値：'予想到着時間: 注文から約', '分後', '.0f'。
# TODO 50：次の処理を実行してください。 使用する処理：print。 主な指定値：'通常の誤差幅を考慮した案内例: 約', '〜', '分後', '.0f'。
# TODO 51：fig, axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, 12, 5。
# TODO 52：次の処理を実行してください。 使用する処理：scatter。 主な指定値：0.7, '#4C78A8', 0。
# TODO 53：value_min を作成・更新してください。 使用する処理：min, y_test.min, predicted.min。
# TODO 54：value_max を作成・更新してください。 使用する処理：max, y_test.max, predicted.max。
# TODO 55：次の処理を実行してください。 使用する処理：plot。 主な指定値：'--', '#E45756', 'Perfect prediction', 0。
# TODO 56：次の処理を実行してください。 使用する処理：set_xlabel。 主な指定値：'Actual delivery time (minutes)', 0。
# TODO 57：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Predicted delivery time (minutes)', 0。
# TODO 58：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Actual vs Predicted', 0。
# TODO 59：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 0。
# TODO 60：次の処理を実行してください。 使用する処理：legend。 主な指定値：0。
# TODO 61：residuals を作成・更新してください。
# TODO 62：次の処理を実行してください。 使用する処理：scatter。 主な指定値：0.7, '#54A24B', 1。
# TODO 63：次の処理を実行してください。 使用する処理：axhline。 主な指定値：0, '#E45756', '--', 1。
# TODO 64：次の処理を実行してください。 使用する処理：set_xlabel。 主な指定値：'Predicted delivery time (minutes)', 1。
# TODO 65：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Residual: actual - predicted (minutes)', 1。
# TODO 66：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Residual Plot', 1。
# TODO 67：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 1。
# TODO 68：次の処理を実行してください。 使用する処理：fig.tight_layout。
# TODO 69：次の処理を実行してください。 使用する処理：plt.show。
# TODO 70：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【実務上の注意】'。
# TODO 71：次の処理を実行してください。 使用する処理：print。 主な指定値：'予測値は確定時刻ではありません。交通事故、店舗混雑、住所確認など、'。
# TODO 72：次の処理を実行してください。 使用する処理：print。 主な指定値：'データにない要因でも遅れるため、幅を持たせて案内することが重要です。'。
#
# 【使用する名前・データ仕様】
# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。
# ・Actual vs Predicted / actual_minutes / axes / axhline / binomial / clip / coefficient_minutes / coefficient_table
# ・copy / courier_active_orders / DataFrame / default_rng / deliveries / delivery_minutes / distance_km / drop
# ・error_minutes / feature / fit / grid / head / integers / is_raining / item_count
# ・legend / LinearRegression / mae / max / mean / mean_absolute_error / mean_squared_error / min
# ・new_order / new_prediction / noise / normal / number_of_orders / Perfect prediction / plot / predict
# ・predicted / predicted_minutes / r2_score / Residual Plot / residuals / restaurant_prep_minutes / rmse / rng
# ・round / scatter / set_title / set_xlabel / set_ylabel / show / sort_values / sqrt
# ・subplots / tight_layout / to_string / traffic_level / train_test_split / uniform / value_max / value_min
# ・X_test / X_train / y_test / y_train
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
