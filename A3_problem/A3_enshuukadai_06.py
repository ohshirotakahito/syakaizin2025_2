# -*- coding: utf-8 -*-
"""
6. 温度変換ツール:

（課題）
セ氏温度を華氏温度に変換する関数celsius_to_fahrenheitを作成する。
華氏温度をセ氏温度に変換する関数fahrenheit_to_celsiusを作成する。
これらの関数を使用して、複数の温度データに対して変換を行う。
"""

def celsius_to_fahrenheit(celsius):
    """ セ氏温度を華氏温度に変換する """
    # TODO: ここに実装してください
    pass

def fahrenheit_to_celsius(fahrenheit):
    """ 華氏温度をセ氏温度に変換する """
    # TODO: ここに実装してください
    pass

# 温度データの例
celsius_temperatures = [0, 20, 30, 100]
fahrenheit_temperatures = [32, 68, 86, 212]

# セ氏から華氏への変換
print("セ氏から華氏への変換:")
for c in celsius_temperatures:
    print(f"{c}°C = {celsius_to_fahrenheit(c)}°F")

# 華氏からセ氏への変換
print("\n華氏からセ氏への変換:")
for f in fahrenheit_temperatures:
    print(f"{f}°F = {fahrenheit_to_celsius(f)}°C")
