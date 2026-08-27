# -*- coding: utf-8 -*-
"""
D1 演習課題7（問題版）：工場設備の故障を予測するモデルを選ぼう
==========================================================

食品工場の予知保全担当者として、24時間以内の設備故障を予測します。
3種類の分類モデルを公平に比較し、業務目的に合うモデルを選んでください。
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, recall_score
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# データ生成部分は完成済みです。
rng = np.random.default_rng(42)
n = 800
temperature_c = np.clip(rng.normal(68, 9, n), 35, 105)
vibration_mm_s = np.clip(rng.gamma(2.2, 1.4, n), 0.2, 14)
pressure_kpa = np.clip(rng.normal(205, 25, n), 120, 290)
motor_current_a = np.clip(rng.normal(18, 4, n), 7, 34)
hours_since_maintenance = rng.integers(10, 1500, n)
production_speed = np.clip(rng.normal(92, 15, n), 45, 135)
failure_score = (
    -4.0 + 0.055 * (temperature_c - 65) + 0.42 * (vibration_mm_s - 3)
    + 0.045 * (motor_current_a - 18)
    + 0.0018 * (hours_since_maintenance - 600)
    + 0.018 * (production_speed - 90)
    + 0.0007 * (pressure_kpa - 205) ** 2
)
failure_probability = 1 / (1 + np.exp(-failure_score))
failure_within_24h = rng.binomial(1, failure_probability)
machines = pd.DataFrame({
    "temperature_c": temperature_c.round(1),
    "vibration_mm_s": vibration_mm_s.round(2),
    "pressure_kpa": pressure_kpa.round(1),
    "motor_current_a": motor_current_a.round(1),
    "hours_since_maintenance": hours_since_maintenance,
    "production_speed": production_speed.round(1),
    "failure_within_24h": failure_within_24h,
})


# 問題1：データの先頭、件数、故障率を表示してください。
# TODO：


# 問題2：目的変数をy、それ以外をXへ代入し、学習75%・テスト25%へ
# 分割してください。random_state=42、stratify=yを指定します。
# TODO：


# 【選択問題1】stratify=yを指定する目的はどれですか。
# A. 学習用とテスト用の故障率をほぼ同じにする
# B. 故障データを削除する
# C. 特徴量を標準化する
# D. 必ず正解率を100%にする
# 答え：


# 問題3：次の3モデルをmodelsという辞書に用意してください。
# ・StandardScaler + LogisticRegression
# ・StandardScaler + KNeighborsClassifier
# ・RandomForestClassifier
# TODO：


# 【選択問題2】ランダムフォレストで標準化が通常不要なのはなぜですか。
# A. 特徴量の大小関係で分岐する木を使い、距離を直接計算しないから
# B. データを1列しか使わないから
# C. 目的変数が不要だから
# D. 常に同じ予測をするから
# 答え：


# 問題4：各モデルを5分割交差検証し、accuracy、recall、roc_aucの
# 平均を表にしてください。cross_validate()を使用します。
# TODO：


# 【選択問題3】交差検証を使う理由として適切なものはどれですか。
# A. 1回の分割結果だけに依存せず、性能を安定して比較するため
# B. データを水増しするため
# C. 故障を修理するため
# D. グラフを必ず描くため
# 答え：


# 問題5：故障クラスのrecallが最大のモデルを選び、全学習データで
# 学習して、テストデータを予測してください。
# TODO：


# 【選択問題4】故障クラスのrecallが低いと、何が起こりますか。
# A. 実際の故障を正常と予測する見逃しが増える
# B. 正常設備がすべて故障する
# C. センサーの数が減る
# D. 学習時間が必ず短くなる
# 答え：


# 問題6：モデル比較の棒グラフと、採用モデルの混同行列を表示します。
# TODO：


# 【考察問題】
# 1. 故障の見逃しと誤警報では、どちらのコストが大きいでしょうか。
#    工場の状況を想定して説明してください。
# 答え：

# 2. 予測に追加したいセンサーや記録を2つ以上挙げてください。
# 答え：

# 3. モデルの予測だけで設備を即時停止してよいでしょうか。
#    現場で必要な確認手順を考えてください。
# 答え：

# === 解答対応ガイド（自動照合済み） ===
#
# 【このガイドの目的】
# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、
# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。
#
# 【解答版に含まれる背景・ヒント】
# ・再現可能な架空センサーデータを800件生成します。
# ・高温・振動・電流・整備後時間などから故障確率を生成します。
# ・説明変数Xと目的変数yを分け、最終評価用のテストデータを確保します。
# ・距離や係数を使う2モデルは標準化とPipelineでつなぎます。
# ・木構造を使うランダムフォレストは、通常は標準化が不要です。
# ・故障の見逃しを重視するためrecallを中心に、accuracyとROC-AUCも評価します。
# ・学習データ内で5分割交差検証を行います。
# ・今回は故障の見逃しを減らす目的なので、recall最大のモデルを選びます。
# ・採用モデルを全学習データで学習し、未使用のテストデータで最終評価します。
# ・左にモデル比較、右に採用モデルの混同行列を表示します。
#
# 【実装課題：解答版との対応順】
# TODO 01：必要なライブラリまたは機能 matplotlib.pyplot（別名 plt） を読み込んでください。
# TODO 02：必要なライブラリまたは機能 numpy（別名 np） を読み込んでください。
# TODO 03：必要なライブラリまたは機能 pandas（別名 pd） を読み込んでください。
# TODO 04：必要なライブラリまたは機能 sklearn.ensemble.RandomForestClassifier を読み込んでください。
# TODO 05：必要なライブラリまたは機能 sklearn.linear_model.LogisticRegression を読み込んでください。
# TODO 06：必要なライブラリまたは機能 sklearn.metrics.ConfusionMatrixDisplay, sklearn.metrics.classification_report, sklearn.metrics.recall_score を読み込んでください。
# TODO 07：必要なライブラリまたは機能 sklearn.model_selection.cross_validate, sklearn.model_selection.train_test_split を読み込んでください。
# TODO 08：必要なライブラリまたは機能 sklearn.neighbors.KNeighborsClassifier を読み込んでください。
# TODO 09：必要なライブラリまたは機能 sklearn.pipeline.make_pipeline を読み込んでください。
# TODO 10：必要なライブラリまたは機能 sklearn.preprocessing.StandardScaler を読み込んでください。
# TODO 11：rng を作成・更新してください。 使用する処理：np.random.default_rng。 主な指定値：42。
# TODO 12：n を作成・更新してください。 主な指定値：800。
# TODO 13：temperature_c を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：35, 105, 68, 9。
# TODO 14：vibration_mm_s を作成・更新してください。 使用する処理：np.clip, rng.gamma。 主な指定値：0.2, 14, 2.2, 1.4。
# TODO 15：pressure_kpa を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：120, 290, 205, 25。
# TODO 16：motor_current_a を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：7, 34, 18, 4。
# TODO 17：hours_since_maintenance を作成・更新してください。 使用する処理：rng.integers。 主な指定値：10, 1500。
# TODO 18：production_speed を作成・更新してください。 使用する処理：np.clip, rng.normal。 主な指定値：45, 135, 92, 15。
# TODO 19：failure_score を作成・更新してください。 主な指定値：0.0007, 0.018, 2, 0.0018, 90, 205, 0.045, 600, 0.42, 18, 4.0, 0.055。
# TODO 20：failure_probability を作成・更新してください。 使用する処理：np.exp。 主な指定値：1。
# TODO 21：failure_within_24h を作成・更新してください。 使用する処理：rng.binomial。 主な指定値：1。
# TODO 22：machines を作成・更新してください。 使用する処理：pd.DataFrame, temperature_c.round, vibration_mm_s.round, pressure_kpa.round, motor_current_a.round, production_speed.round。 主な指定値：'temperature_c', 'vibration_mm_s', 'pressure_kpa', 'motor_current_a', 'hours_since_maintenance', 'production_speed', 'failure_within_24h', 1, 2。
# TODO 23：次の処理を実行してください。 使用する処理：print。 主な指定値：'【設備データ】'。
# TODO 24：次の処理を実行してください。 使用する処理：print, machines.head。
# TODO 25：次の処理を実行してください。 使用する処理：print, mean。 主な指定値：'\n故障率: ', '.1%', 'failure_within_24h'。
# TODO 26：X を作成・更新してください。 使用する処理：machines.drop。 主な指定値：'failure_within_24h'。
# TODO 27：y を作成・更新してください。 主な指定値：'failure_within_24h'。
# TODO 28：X_train, X_test, y_train, y_test を作成・更新してください。 使用する処理：train_test_split。 主な指定値：0.25, 42。
# TODO 29：models を作成・更新してください。 使用する処理：make_pipeline, RandomForestClassifier, StandardScaler, LogisticRegression, KNeighborsClassifier。 主な指定値：'Logistic regression', 'k-NN', 'Random forest', 250, 42, 'balanced', 2000, 9, 'distance'。
# TODO 30：scoring を作成・更新してください。 主な指定値：'accuracy', 'recall', 'roc_auc'。
# TODO 31：comparison_rows を作成・更新してください。
# TODO 32：models.items() を順に処理する反復を作ってください。 使用する処理：models.items, cross_validate, comparison_rows.append, mean。 主な指定値：5, 'model', 'accuracy', 'recall', 'roc_auc', 'test_accuracy', 'test_recall', 'test_roc_auc'。
# TODO 33：comparison を作成・更新してください。 使用する処理：set_index, pd.DataFrame。 主な指定値：'model'。
# TODO 34：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n【5分割交差検証の平均】'。
# TODO 35：次の処理を実行してください。 使用する処理：print, comparison.round。 主な指定値：3。
# TODO 36：best_model_name を作成・更新してください。 使用する処理：idxmax。 主な指定値：'recall'。
# TODO 37：best_model を作成・更新してください。
# TODO 38：次の処理を実行してください。 使用する処理：print。 主な指定値：'\n採用モデル: ', '（再現率を重視）'。
# TODO 39：次の処理を実行してください。 使用する処理：best_model.fit。
# TODO 40：test_prediction を作成・更新してください。 使用する処理：best_model.predict。
# TODO 41：test_recall を作成・更新してください。 使用する処理：recall_score。
# TODO 42：次の処理を実行してください。 使用する処理：print。 主な指定値：'テストデータの故障再現率: ', '.3f'。
# TODO 43：次の処理を実行してください。 使用する処理：print, classification_report。 主な指定値：0, 'Normal', 'Failure'。
# TODO 44：fig, axes を作成・更新してください。 使用する処理：plt.subplots。 主な指定値：1, 2, 13, 5。
# TODO 45：次の処理を実行してください。 使用する処理：comparison.plot。 主な指定値：'bar', 0, 1, '#4C78A8', '#F58518', '#54A24B'。
# TODO 46：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Cross-validation Model Comparison', 0。
# TODO 47：次の処理を実行してください。 使用する処理：set_ylabel。 主な指定値：'Score', 0。
# TODO 48：次の処理を実行してください。 使用する処理：tick_params。 主な指定値：'x', 15, 0。
# TODO 49：次の処理を実行してください。 使用する処理：grid。 主な指定値：'y', 0.25, 0。
# TODO 50：次の処理を実行してください。 使用する処理：legend。 主な指定値：'lower right', 0。
# TODO 51：次の処理を実行してください。 使用する処理：ConfusionMatrixDisplay.from_predictions。 主な指定値：'Oranges', 'Normal', 'Failure', 1。
# TODO 52：次の処理を実行してください。 使用する処理：set_title。 主な指定値：'Selected Model: ', 1。
# TODO 53：次の処理を実行してください。 使用する処理：fig.tight_layout。
# TODO 54：次の処理を実行してください。 使用する処理：plt.show。
# TODO 55：次の処理を実行してください。 使用する処理：print。 主な指定値：'【実務上の判断】'。
# TODO 56：次の処理を実行してください。 使用する処理：print。 主な指定値：'故障の見逃しは停止・廃棄・安全事故につながるため、正解率だけでなく'。
# TODO 57：次の処理を実行してください。 使用する処理：print。 主な指定値：'故障クラスの再現率を重視します。一方、誤警報による点検コストとの'。
# TODO 58：次の処理を実行してください。 使用する処理：print。 主な指定値：'バランスも、運用開始前に現場と決める必要があります。'。
#
# 【使用する名前・データ仕様】
# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。
# ・accuracy / append / axes / balanced / best_model / best_model_name / binomial / candidate_model
# ・classification_report / clip / comparison / comparison_rows / Cross-validation Model Comparison / cross_validate / DataFrame / default_rng
# ・distance / drop / exp / Failure / failure_probability / failure_score / failure_within_24h / fit
# ・from_predictions / gamma / grid / head / hours_since_maintenance / idxmax / integers / items
# ・k-NN / KNeighborsClassifier / legend / Logistic regression / LogisticRegression / lower right / machines / make_pipeline
# ・mean / model / models / motor_current_a / name / Normal / normal / Oranges
# ・plot / predict / pressure_kpa / production_speed / Random forest / RandomForestClassifier / recall / recall_score
# ・rng / roc_auc / round / Score / scores / scoring / set_index / set_title
# ・set_ylabel / show / StandardScaler / subplots / temperature_c / test_accuracy / test_prediction / test_recall
# ・test_roc_auc / tick_params / tight_layout / train_test_split / vibration_mm_s / X_test / X_train / y_test
# ・y_train
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
