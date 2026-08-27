# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Fri Nov 17 11:39:34 2023

@author: ohshi
"""
# =============================================================================
# ５．ランダムウォークによる粒子の拡散のシミュレーション:
# 
# 実験結果の不確実性を評価するためにモンテカルロシミュレーションを用いる場面がある。そこで，今回は，粒子の拡散シュミレーションを行ってください．
# 
# 目的：
# 
# 2次元空間での粒子のランダムウォークをシミュレートする。
# 時間経過に伴う粒子の位置変化を観察し、拡散の概念を理解する。
# 
# 問題設定：
# 
# 2次元空間（x-y平面）で、一つの粒子がランダムに動く状況を考える。
# 各ステップで粒子は上下左右のいずれかの方向に一定の距離（例えば1単位）動く。
# シミュレーションはNステップ行い、各ステップでの粒子の位置を記録する。
# 
# 実装手順：
# 
# 必要なPythonライブラリ（例：numpy, matplotlib）をインポートする。
# 粒子の初期位置（例：原点）を設定する。
# 各ステップでの粒子の動きをランダムに決定し、その位置を更新する関数を作成する。
# Nステップのシミュレーションを行い、各ステップでの位置を記録する。
# 結果をプロットして、粒子の軌跡を視覚化する。
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# パラメータの設定
N = 1000  # ステップ数
x, y = 0, 0  # 初期位置

# 各ステップでの位置を記録するリスト
x_positions = [x]
y_positions = [y]

# ランダムウォークのシミュレーション
for _ in range(N):
    step = np.random.choice(['up', 'down', 'left', 'right'])
    if step == 'up':
        y += 1
    elif step == 'down':
        y -= 1
    elif step == 'left':
        x -= 1
    else:
        x += 1
    x_positions.append(x)
    y_positions.append(y)

# 結果のプロット
plt.plot(x_positions, y_positions)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Random Walk of a Particle in 2D Space')
plt.show()
