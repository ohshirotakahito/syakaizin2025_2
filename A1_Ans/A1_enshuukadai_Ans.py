# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 20:09:27 2023

@author: toshiro
"""

# 解答版：店舗の日次業務を題材に、変数・型・演算・条件分岐・反復を学びます。
##1.変数の定義
#整数10を変数aに、浮動小数点数20.5を変数bにそれぞれ代入してください。

#変数a,bの定義
a = 10
b = 20.5
#a, bの表示
print(a,b)


##２．基本的なデータ型の表示
##変数cに文字列"Hello, World!"を代入し、変数cのデータ型を確認してください。

c = "Hello, World!"
#cの表示
print(c)

#基本的なデータ型
print(type(c))

#３．演算子による計算
#変数aとbの合計、差、積、商を計算してください。
print(a + b, a - b, a * b, a / b)

#4.条件分岐
#　変数aが10以上であれば"a is 10 or more"と表示し、それ以外の場合は"a is less than 10"と表示するプログラムを作成してください。
if a >= 10:
    print("a is 10 or more")
else:
    print("a is less than 10")
    
#5.ループ
#forループを使用して、1から10までの整数を順番に表示するプログラムを作成してください。
for i in range(1, 11):
    print(i)

#6.リスト
#リストdを作成し、その中に1, 2, 3, 4, 5の5つの整数を格納してください。
d = [1, 2, 3, 4, 5]
print(d)

#7.リストの操作
#リストdの最後に整数6を追加し、リストdの内容を表示してください。
d.append(6)
print(d)

#8.文字列の操作
#変数cの文字列を全て大文字にし、結果を表示してください。cは"Hello, World!"なのでHELLO, WORLDが正解
c_upper = c.upper()
print(c_upper)

#9.関数の定義
#引数を2つ取り、その合計を返す関数sum_two_numbersを定義してください。
def sum_two_numbers(num1, num2):
    return num1 + num2

#10.関数の呼び出し
#上記定義関数sum_two_numbersを使用し、10と20の合計結果を表示してください。
sum_result = sum_two_numbers(10, 20)
print(sum_result)

