# -*- coding: utf-8 -*-
"""
D1 演習課題5（問題版）：サブスク顧客の解約を予測しよう
====================================================

【あなたの役割】
あなたは動画配信サービスのカスタマーサクセス担当者です。翌月に解約する
可能性が高い顧客を予測し、早めのサポートにつなげてください。

TODOへコードを書き、選択問題と考察問題にも答えてください。
データは演習用に生成した架空データです。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# 架空データを作る部分は完成済みです。変更せずに使用してください。
rng = np.random.default_rng(42)
number_of_customers = 500
tenure_months = rng.integers(1, 73, number_of_customers)
monthly_fee_yen = np.clip(rng.normal(7200, 1800, number_of_customers), 2500, 13000)
support_tickets = np.clip(rng.poisson(1.8, number_of_customers), 0, 9)
weekly_hours = np.clip(rng.normal(8.5, 4.0, number_of_customers), 0.2, 25)
payment_delays = np.clip(rng.poisson(0.7, number_of_customers), 0, 6)
contract_months = rng.choice([1, 12, 24], number_of_customers, p=[0.45, 0.35, 0.20])

churn_score = (
    0.3
    - 0.025 * tenure_months
    + 0.00022 * (monthly_fee_yen - 7000)
    + 0.28 * support_tickets
    - 0.055 * weekly_hours
    + 0.45 * payment_delays
    - 0.055 * contract_months
)
churn_probability = 1 / (1 + np.exp(-churn_score))
churn_next_month = rng.binomial(1, churn_probability)

customers = pd.DataFrame({
    "tenure_months": tenure_months,
    "monthly_fee_yen": monthly_fee_yen.round().astype(int),
    "support_tickets": support_tickets,
    "weekly_hours": weekly_hours.round(1),
    "payment_delays": payment_delays,
    "contract_months": contract_months,
    "churn_next_month": churn_next_month,
})


# ==================================================================
# 問題1：目的変数と説明変数を確認する
# ==================================================================
# TODO 1-A：customersの先頭5行、顧客数、解約者数、解約率を表示します。


# TODO 1-B：churn_next_month以外を説明変数Xへ、churn_next_monthを
# 目的変数yへ代入してください。


# 【選択問題1】
# この分析の目的変数はどれですか。
#
# A. monthly_fee_yen
# B. churn_next_month
# C. tenure_months
# D. number_of_customers
#
# 自分の答え：


# 【選択問題2】
# 今回の問題が「分類」である理由はどれですか。
#
# A. 解約・継続というカテゴリを予測するから
# B. 月額料金の平均を計算するから
# C. 顧客を並べ替えるから
# D. グラフを2つ作るから
#
# 自分の答え：


# ==================================================================
# 問題2：学習用とテスト用へ分割する
# ==================================================================
# TODO 2-A：データを学習用75%、テスト用25%へ分けてください。
# random_state=42、stratify=yを指定します。


# 【選択問題3】
# テストデータを分けておく主な理由はどれですか。
#
# A. 未知の顧客に対する予測性能を確かめるため
# B. データの列数を増やすため
# C. 解約者を削除するため
# D. グラフの色を決めるため
#
# 自分の答え：


# ==================================================================
# 問題3：分類モデルを学習する
# ==================================================================
# TODO 3-A：StandardScalerとLogisticRegressionをmake_pipelineで
# つないだモデルを作ってください。max_iter=2000とします。


# TODO 3-B：X_trainとy_trainを使ってモデルを学習してください。


# TODO 3-C：X_testについて、予測クラスをpredicted_classへ、
# 解約確率をpredicted_probabilityへ代入してください。


# 【選択問題4】
# Pipelineで標準化とモデルをつなぐ利点として適切なものはどれですか。
#
# A. 学習と予測で同じ前処理を安全に適用できる
# B. 解約率を必ず100%にできる
# C. テストデータも使って平均を学習できる
# D. 説明変数が不要になる
#
# 自分の答え：


# ==================================================================
# 問題4：モデルを評価する
# ==================================================================
# TODO 4-A：正解率とROC-AUCを計算して表示してください。


# TODO 4-B：classification_reportを表示してください。


# TODO 4-C：混同行列からtn、fp、fn、tpを取り出し、それぞれの人数を
# 表示してください。


# 【選択問題5】
# 「実際は解約したが、モデルは継続と予測した」ケースはどれですか。
#
# A. TN（真陰性）
# B. FP（偽陽性）
# C. FN（偽陰性）
# D. TP（真陽性）
#
# 自分の答え：


# 【考察問題1】
# 解約防止を目的とする場合、FPとFNのどちらを特に減らしたいですか。
# 業務上の理由も説明してください。
# 自分の答え：


# ==================================================================
# 問題5：解約に関係する特徴量を調べる
# ==================================================================
# TODO 5-A：Pipelineからロジスティック回帰モデルを取り出してください。


# TODO 5-B：各説明変数の係数を表にして、絶対値が大きい順に表示します。


# 【選択問題6】
# 標準化後のロジスティック回帰で、係数が大きな正の値なら何を
# 意味しますか。
#
# A. その特徴量が増えるほど解約確率が高くなる方向に関係する
# B. その特徴量は常に0になる
# C. その特徴量がモデルから削除された
# D. その特徴量の単位が円である
#
# 自分の答え：


# ==================================================================
# 問題6：評価結果を可視化する
# ==================================================================
# TODO 6-A：混同行列をグラフにしてください。


# TODO 6-B：ROC曲線を描き、ランダム予測を表す対角線も追加します。


# TODO 6-C：解約確率が高い顧客上位10人を表示してください。


# ==================================================================
# 最終考察
# ==================================================================
# 1. 解約確率の高い顧客へ、どのようなサポートを提案しますか。
# 自分の答え：


# 2. 解約確率が高いという理由だけで、サービス制限や料金変更などの
# 不利益を与えてよいでしょうか。理由も説明してください。
# 自分の答え：


# 3. よりよい予測のために追加したいデータを2つ以上挙げてください。
# 自分の答え：

# === 解答対応ガイド（自動照合済み） ===
#
# 【このガイドの目的】
# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、
# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。
#
# 【解答版に含まれる背景・ヒント】
# ・random_stateを固定し、実行するたびに同じ架空データを作ります。
# ・顧客の利用状況を、現実的な範囲で生成します。
# ・解約しやすさを表す架空のスコアを作ります。
# ・長期利用・長期契約・利用時間の多さは解約を抑える方向、料金・問い合わせ・
# ・支払い遅延は解約を増やす方向に設定しています。
# ・ロジスティック関数でスコアを0から1の解約確率へ変換します。
# ・各顧客について乱数と確率を比較し、翌月解約を0または1で生成します。
# ・分析しやすいよう、すべての項目をDataFrameにまとめます。
# ・Xは予測に使う説明変数、yは予測したい目的変数です。
# ・学習用75%、テスト用25%に分けます。
# ・stratify=yにより、学習用とテスト用の解約率をほぼ同じに保ちます。
# ・標準化とロジスティック回帰をPipelineで一つにつなぎます。
# ・Pipelineにすると、テストデータへ学習用データの基準で標準化を適用でき、
# ・テストデータの情報が学習へ漏れる「データリーク」を防げます。
# ・学習用データから、解約と各特徴量の関係を学習します。
# ・predict()は0または1、predict_proba()は解約確率を返します。
# ・正解率は全予測のうち正しかった割合です。
# ・ROC-AUCは、解約者を継続者より高リスクと順位付けできる能力を表します。
# ・0.5はランダムに近く、1.0に近いほど識別能力が高いことを示します。
# ・混同行列から、4種類の予測結果を取り出します。
# ・Pipeline内のロジスティック回帰モデルを取り出します。
# ・標準化後の係数なので、絶対値で特徴量同士の影響を比較できます。
# ・正の係数は解約確率を上げる方向、負の係数は下げる方向です。
# ・混同行列とROC曲線を横に並べます。
# ・解約確率が高い順に、テストデータの要フォロー顧客を表示します。
#
# 【実装課題：解答版との対応順】
# TODO 01：必要なライブラリまたは機能 matplotlib.pyplot（別名 plt） を読み込んでください。
# TODO 02：必要なライブラリまたは機能 numpy（別名 np） を読み込んでください。
# TODO 03：必要なライブラリまたは機能 pandas（別名 pd） を読み込んでください。
# TODO 04：必要なライブラリまたは機能 sklearn.linear_model.LogisticRegression を読み込んでください。
# TODO 05：必要なライブラリまたは機能 sklearn.metrics.ConfusionMatrixDisplay, sklearn.metrics.RocCurveDisplay, sklearn.metrics.accuracy_score, sklearn.metrics.classification_report, sklearn.metrics.confusion_matrix, sklearn.metrics.roc_auc_score を読み込んでください。
# TODO 06：必要なライブラリまたは機能 sklearn.model_selection.train_test_split を読み込んでください。
# TODO 07：必要なライブラリまたは機能 sklearn.pipeline.make_pipeline を読み込んでください。
# TODO 08：必要なライブラリまたは機能 sklearn.preprocessing.StandardScaler を読み込んでください。
# TODO 09：rng を作成・更新してください。 使用する処理：np.random.default_rng。 主な指定値：42。
# TODO 10：number_of_customers を作成・更新してください。 主な指定値：500。
# TODO 11：tenure_months を作成・更新してください。 使用する処理：rng.integers。 主な指定値：1, 73。
# TODO 12：monthly_fee_yen を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：2500, 13000, 7200, 1800。
# TODO 13：support_tickets を作成・更新してください。 使用する処理：np.clip, rng.poisson。 主な指定値：0, 9, 1.8。
# TODO 14：weekly_hours を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：0.2, 25, 8.5, 4.0。
# TODO 15：payment_delays を作成・更新してください。 使用する処理：np.clip, rng.poisson。 主な指定値：0, 6, 0.7。
# TODO 16：contract_months を作成・更新してください。 使用する処理：rng.choice。 主な指定値：1, 12, 24, 0.45, 0.35, 0.2。
# TODO 17：churn_score を作成・更新してください。 主な指定値：0.055, 0.45, 0.28, 0.3, 0.00022, 0.025, 7000。
# TODO 18：churn_probability を作成・更新してください。 使用する処理：np.exp。 主な指定値：1。
# TODO 19：churn_next_month を作成・更新してください。 使用する処理：rng.binomial。 主な指定値：1。
# TODO 20：customers を作成・更新してください。 使用する処理：pd.DataFrame, astype, weekly_hours.round, monthly_fee_yen.round。 主な指定値：'tenure_months', 'monthly_fee_yen', 'support_tickets', 'weekly_hours', 'payment_delays', 'contract_months', 'churn_next_month', 1。
# TODO 21：次の処理を実行してください。 使用する処理：print。 主な指定値：'【顧客データ：先頭5行】'。
# TODO 22：次の処理を実行してください。 使用する処理：print, customers.head。
# TODO 23：次の処理を実行してください。 使用する処理：print, len。 主な指定値：'\n顧客数: ', '人'。
# TODO 24：次の処理を実行してください。 使用する処理：print, sum。 主な指定値：'解約者数: ', '人', 'churn_next_month'。
# TODO 25：次の処理を実行してください。 使用する処理：print, mean。 主な指定値：'解約率: ', '.1%', 'churn_next_month'。
# TODO 26：X を作成・更新してください。 使用する処理：customers.drop。 主な指定値：'churn_next_month'。
# TODO 27：y を作成・更新してください。 主な指定値：'churn_next_month'。
# TODO 28：X_train, X_test, y_train, y_test を作成・更新してください。 使用する処理：train_test_split。 主な指定値：0.25, 42。
# TODO 29：model を作成・更新してください。 使用する処理：make_pipeline, StandardScaler, LogisticRegression。 主な指定値：2000。
# TODO 30：次の処理を実行してください。 使用する処理：model.fit。
# TODO 31：predicted_class を作成・更新してください。 使用する処理：model.predict。
# TODO 32：predicted_probability を作成・更新してください。 使用する処理：model.predict_proba。 主な指定値：1。
# TODO 33：accuracy を作成・更新してください。 使用する処理：accuracy_score。
# TODO 34：auc を作成・更新してください。 使用する処理：roc_auc_score。
# TODO 35：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【モデル評価】'。
# TODO 36：次の処理を実行してください。 使用する処理：print。 主な指定値：'正解率: ', '.3f'。
# TODO 37：次の処理を実行してください。 使用する処理：print。 主な指定値：'ROC-AUC: ', '.3f'。
# TODO 38：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【分類レポート】'。
# TODO 39：次の処理を実行してください。 使用する処理：print, classification_report。 主な指定値：0, '継続', '解約'。
# TODO 40：tn, fp, fn, tp を作成・更新してください。 使用する処理：ravel, confusion_matrix。
# TODO 41：次の処理を実行してください。 使用する処理：print。 主な指定値：'【混同行列の読み取り】'。
# TODO 42：次の処理を実行してください。 使用する処理：print。 主な指定値：'継続を正しく予測: ', '人'。
# TODO 43：次の処理を実行してください。 使用する処理：print。 主な指定値：'継続者を解約と誤予測: ', '人'。
# TODO 44：次の処理を実行してください。 使用する処理：print。 主な指定値：'解約者を見逃し: ', '人'。
# TODO 45：次の処理を実行してください。 使用する処理：print。 主な指定値：'解約を正しく予測: ', '人'。
# TODO 46：logistic_model を作成・更新してください。 主な指定値：'logisticregression'。
# TODO 47：coefficients を作成・更新してください。 使用する処理：pd.Series。 主な指定値：0。
# TODO 48：coefficient_table を作成・更新してください。 使用する処理：sort_values, pd.DataFrame, coefficients.abs。 主な指定値：'absolute_importance', False, 'coefficient'。
# TODO 49：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【解約予測へ影響した特徴量】'。
# TODO 50：次の処理を実行してください。 使用する処理：print, coefficient_table.round。 主な指定値：3。
# TODO 51：fig, axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, 12, 5。
# TODO 52：次の処理を実行してください。 使用する処理：ConfusionMatrixDisplay.from_predictions。 主な指定値：'Blues', 'Continue', 'Churn', 0。
# TODO 53：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Churn Prediction: Confusion Matrix', 0。
# TODO 54：次の処理を実行してください。 使用する処理：RocCurveDisplay.from_predictions。 主な指定値：'Logistic regression (AUC=', ')', 1, '.3f'。
# TODO 55：次の処理を実行してください。 使用する処理：plot。 主な指定値：'--', 0, 1, 'gray', 'Random'。
# TODO 56：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'ROC Curve', 1。
# TODO 57：次の処理を実行してください。 使用する処理：grid。 主な指定値：0.25, 1。
# TODO 58：次の処理を実行してください。 使用する処理：legend。 主な指定値：1。
# TODO 59：次の処理を実行してください。 使用する処理：fig.tight_layout。
# TODO 60：次の処理を実行してください。 使用する処理：plt.show。
# TODO 61：follow_up を作成・更新してください。 使用する処理：X_test.copy。
# TODO 62：指定された変数 を作成・更新してください。 主な指定値：'actual_churn'。
# TODO 63：指定された変数 を作成・更新してください。 主な指定値：'predicted_probability'。
# TODO 64：follow_up を作成・更新してください。 使用する処理：follow_up.sort_values。 主な指定値：'predicted_probability', False。
# TODO 65：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【優先フォロー候補：上位10人】'。
# TODO 66：次の処理を実行してください。 使用する処理：print, round, follow_up.head。 主な指定値：3, 10。
# TODO 67：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【実務上の注意】'。
# TODO 68：次の処理を実行してください。 使用する処理：print。 主な指定値：'予測確率は解約の確定ではありません。顧客への不利益な判断には使わず、'。
# TODO 69：次の処理を実行してください。 使用する処理：print。 主な指定値：'サポート案内や満足度確認など、顧客体験を改善する目的で利用します。'。
#
# 【使用する名前・データ仕様】
# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。
# ・abs / absolute_importance / accuracy / accuracy_score / actual_churn / astype / auc / axes
# ・binomial / Blues / choice / Churn / churn_next_month / churn_probability / churn_score / classification_report
# ・clip / coefficient / coefficient_table / coefficients / confusion_matrix / Continue / contract_months / copy
# ・customers / DataFrame / default_rng / drop / exp / fit / follow_up / from_predictions
# ・gray / grid / head / integers / legend / logistic_model / LogisticRegression / logisticregression
# ・make_pipeline / mean / monthly_fee_yen / normal / number_of_customers / payment_delays / plot / poisson
# ・predict / predict_proba / predicted_class / predicted_probability / Random / ravel / rng / ROC Curve
# ・roc_auc_score / round / Series / set_title / show / sort_values / StandardScaler / subplots
# ・sum / support_tickets / tenure_months / tight_layout / train_test_split / weekly_hours / X_test / X_train
# ・y_test / y_train
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
