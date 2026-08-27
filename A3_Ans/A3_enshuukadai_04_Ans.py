# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:18:02 2023

@author: ohshi
"""

# =============================================================================
# 解答版：配送地点が営業拠点の担当範囲内か判定する座標計算
# 4. ジオメトリックツール:
# 
# （課題）
# 二次元座標上の点を表すPointクラスを作成する。
# 2点間の距離を計算する関数calculate_distanceを作成する。
# 点が特定の円の中にあるかどうかを判断する関数is_inside_circleを作成する。
# 
# =============================================================================
import math

class Point:
    def __init__(self, x=0, y=0):
        """ 点の初期化 """
        self.x = x
        self.y = y

def calculate_distance(point1, point2):
    """ 2点間の距離を計算 """
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def is_inside_circle(point, circle_center, radius):
    """ 点が円の中にあるかどうかを判断 """
    distance = calculate_distance(point, circle_center)
    return distance <= radius

# 点と円の例
point1 = Point(1, 2)
point2 = Point(4, 6)
circle_center = Point(3, 3)
radius = 5

# 2点間の距離を計算
distance = calculate_distance(point1, point2)
print(f"点({point1.x}, {point1.y})と点({point2.x}, {point2.y})の距離は {distance} です。")

# 点が円の中にあるかを判断
inside = is_inside_circle(point1, circle_center, radius)
print(f"点({point1.x}, {point1.y})は半径{radius}の円の中に{'あります' if inside else 'ありません'}。")




