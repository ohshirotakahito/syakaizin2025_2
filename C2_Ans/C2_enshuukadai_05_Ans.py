# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#５．ロジスティック回帰:
#
#以下のデータセットが与えられたとき、ロジスティック回帰を利用して、目的変数yを予測するモデルを構築し、そのモデルの精度を評価してください。
#x = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
#y = [0, 0, 1, 1, 1]

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# データセット
x = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
y = [0, 0, 1, 1, 1]

# データセットをトレーニングセットとテストセットに分割
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# ロジスティック回帰モデルの作成と訓練
log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)

# テストセットでモデルを評価
y_pred = log_reg.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)

# モデルの精度を表示
print(f'Accuracy: {accuracy * 100:.2f}%')




