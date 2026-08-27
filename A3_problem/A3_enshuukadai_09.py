# -*- coding: utf-8 -*-
"""
9. シンプルな電卓アプリケーション:

（課題）
2つの数値を入力として受け取り、その数値に対する基本的な算術演算（加算、減算、乗算、除算）を実行する関数群を作成する。
これらの関数を使用して、ユーザーからの入力に基づいて計算を行うインタラクティブなプログラムを作成する。
"""

def add(x, y):
    """ 加算 """
    # TODO: ここに実装してください
    pass

def subtract(x, y):
    """ 減算 """
    # TODO: ここに実装してください
    pass

def multiply(x, y):
    """ 乗算 """
    # TODO: ここに実装してください
    pass

def divide(x, y):
    """ 除算（0で割る場合は「0で割ることはできません。」を返す） """
    # TODO: ここに実装してください
    pass

def main():
    while True:
        try:
            x = float(input("数値1を入力してください: "))
            y = float(input("数値2を入力してください: "))
        except ValueError:
            print("有効な数値を入力してください。")
            continue

        operation = input("演算を選択してください (加算: +, 減算: -, 乗算: *, 除算: /): ")

        if operation == '+':
            print("結果:", add(x, y))
        elif operation == '-':
            print("結果:", subtract(x, y))
        elif operation == '*':
            print("結果:", multiply(x, y))
        elif operation == '/':
            print("結果:", divide(x, y))
        else:
            print("無効な演算です。")

        next_calculation = input("もう一度計算しますか？ (はい/いいえ): ")
        if next_calculation.lower() != 'はい':
            break

if __name__ == "__main__":
    main()
