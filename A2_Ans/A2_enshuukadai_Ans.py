from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
# 解答版：商品マスターと注文情報を題材に、コレクション型を学びます。
#１．タプル:
#以下の要素を持つタプルeを作成してください: 10, 20, 30, 40, 50

e = (10, 20, 30, 40, 50)
print(e)


#２．タプルとリストの変換:
#タプルeをリストに変換し、結果を表示してください。

e_list = list(e)
print(e_list)


#３．辞書:
#．キーと値のペアを持つ辞書fを作成してください。例: {'apple': 1, 'banana': 2, 'cherry': 3}

f = {'apple': 1, 'banana': 2, 'cherry': 3}
print(f)

#４．辞書の操作:
#辞書fに新しいキーと値のペアを追加し、辞書fの内容を表示してください。

f['date'] = 4
print(f)


#５．セット:
#以下の要素を持つセットgを作成してください: 1, 2, 3, 4, 5

g = {1, 2, 3, 4, 5}
print(g)


#６．セットの操作:
#セットgに新しい要素6を追加し、セットgの内容を表示してください。

g.add(6)
print(g)


#７．whileループ:
#whileループを使って、1から10までの整数を順番に表示するプログラムを作成してください。

i = 1
while i <= 10:
    print(i)
    i += 1


#８．リスト内包表記:
#リスト内包表記を使って、1から10までの整数のリストhを作成してください。

h = [i for i in range(1, 11)]
print(h)


#９．関数と条件分岐:
#引数を1つ取り、引数が偶数であれば"Even"、奇数であれば"Odd"を返す関数check_odd_evenを定義してください。

def check_odd_even(num):
    return "Even" if num % 2 == 0 else "Odd"

# Test
print(check_odd_even(4))  # Output: Even
print(check_odd_even(5))  # Output: Odd


#１０．ラムダ関数:
#ラムダ関数を使って、2つの引数の合計を返す関数sum_lambdaを作成してください。

sum_lambda = lambda x, y: x + y

# Test
print(sum_lambda(3, 4))  # Output: 7


#１１．マップ関数:
#リストi = [1, 2, 3, 4, 5] に対して、各要素を2倍にするマップ関数を作成し、結果をリストとして表示してください。

i = [1, 2, 3, 4, 5]
result = list(map(lambda x: x * 2, i))
print(result)


#１２．フィルタ関数:
#リストiから偶数だけをフィルタリングするフィルタ関数を作成し、結果をリストとして表示してください。

result = list(filter(lambda x: x % 2 == 0, i))
print(result)


#１３．モジュールのインポート:
#mathモジュールをインポートし、円周率（π）を表示してください。

import math
print(math.pi)


#１４．例外処理:
#0で除算を試みるコードを書き、ZeroDivisionError例外をキャッチしてエラーメッセージを表示してください。

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")


#１５．ファイル操作:
#"hello.txt"という名前のファイルを作成し、"Hello, World!"というテキストを書き込んでください。そして、そのファイルを読み込み、内容を表示してください。

with open(DATA_DIR / "hello.txt", "w") as file:
    file.write("Hello, World!")

with open(DATA_DIR / "hello.txt", "r") as file:
    content = file.read()
    print(content)
