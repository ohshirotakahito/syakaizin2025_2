# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:18:02 2023

@author: ohshi
"""

# 解答版：コールセンターの応答時間を要約する統計関数
#演習A-3　基本操作と構文（応用）課題
#1. データ分析ツール:
#（課題）
#整数のリストを受け取り、平均値を計算する関数calculate_averageを作成する。
#同じリストを使用して、最大値と最小値を見つける関数find_max_minを作成する。
#これらの関数を使用して、与えられたデータセットの統計情報を分析する。

def calculate_average(numbers):
    """ 整数のリストを受け取り、平均値を計算する """
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def find_max_min(numbers):
    """ 同じリストから最大値と最小値を見つける """
    if len(numbers) == 0:
        return (None, None)
    return (max(numbers), min(numbers))

# データセットの例
data = [10, 20, 30, 40, 50]

# 平均値を計算
average = calculate_average(data)
print(f"平均値: {average}")

# 最大値と最小値を見つける
max_value, min_value = find_max_min(data)
print(f"最大値: {max_value}, 最小値: {min_value}")

