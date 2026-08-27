# -*- coding: utf-8 -*-
"""
D1 演習課題1（解答版）：アヤメのデータを観察しよう
======================================================

Irisデータの読み込みから基本集計までを、一つずつ解説します。
問題版に取り組んだ後で、コードと実行結果を確認してください。
"""

import pandas as pd
from sklearn.datasets import load_iris


# 解答1：IrisデータをPandasの表形式で読み込む
# as_frame=Trueにすると、データをDataFrameとして扱えます。
iris = load_iris(as_frame=True)


# 解答2：target列を意味の分かりやすいspeciesという名前に変更する
df = iris.frame.rename(columns={"target": "species"})

# 品種番号0、1、2をsetosa、versicolor、virginicaに置き換える
df["species"] = df["species"].map(dict(enumerate(iris.target_names)))


# 解答3：head()で先頭5行を表示する
print("【問題4の解答】データの先頭5行")
print(df.head())


# 解答4：shapeから行数と列数を取得する
rows, columns = df.shape
print("\n【問題5の解答】データの大きさ")
print(f"{rows}行、{columns}列です。")


# 解答5：value_counts()で品種ごとの本数を数える
species_counts = df["species"].value_counts()
print("\n【問題6の解答】品種別の本数")
print(species_counts)
print("3品種とも50本ずつあり、件数の偏りはありません。")


# 解答6：groupby()で品種ごとに分け、mean()で平均値を求める
mean_table = df.groupby("species").mean()
print("\n【問題7の解答】品種別の平均値")
print(mean_table.round(2))


# 解答7：項目ごとに最大平均値と最小平均値の差を求める
mean_gaps = mean_table.max() - mean_table.min()

# idxmax()で、差が最大になった項目名を取得する
largest_gap_feature = mean_gaps.idxmax()
print("\n【問題8の解答】")
print(f"平均値の差が最も大きい項目：{largest_gap_feature}")
print(f"最大と最小の平均値の差：{mean_gaps[largest_gap_feature]:.2f} cm")


# 考察例
print("\n【考察例】")
print("花びらの長さ（petal length）と花びらの幅（petal width）は、")
print("品種による平均値の違いがはっきりしています。そのため、この2項目は")
print("3品種を見分けるために役立つ特徴量だと考えられます。")
