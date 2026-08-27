# -*- coding: utf-8 -*-
"""
演習：ロジスティック回帰で2値分類モデルを作る

（課題）
以下のデータセットが与えられたとき、ロジスティック回帰を利用して、
目的変数yを予測するモデルを構築し、そのモデルの精度を評価してください。
x = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
y = [0, 0, 1, 1, 1]

※ 注意：データがわずか5件しかないため、テストデータは1件だけになり、
正解率は0%か100%にしかなりません。書き方を学ぶための最小限の例です。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

x = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
y = [0, 0, 1, 1, 1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

log_reg = LogisticRegression()

# TODO: log_regを学習データx_train, y_trainで学習させてください
# ヒント： log_reg.fit(x_train, y_train)

# TODO: 学習したモデルでx_testを予測し、y_predを求めてください
# ヒント： log_reg.predict(x_test)
# 未学習の間は、すべて0と予測する仮実装にしています。
y_pred = [0] * len(y_test)

accuracy = accuracy_score(y_test, y_pred)

print(f'テストデータ数: {len(y_test)}件')
print(f'Accuracy: {accuracy * 100:.2f}%')
