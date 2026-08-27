# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Fri Nov 17 11:39:34 2023

@author: ohshi
"""
# =============================================================================
# ６．温度と粒子の大きさに依存するランダムウォークのシミュレーション
# 　5を踏まえた拡張を行う．
# 
# 目的：
# 
# ・温度と粒子の大きさがランダムウォークの動きにどのように影響するかを理解する。
# ・粒子の大きさに応じて移動抵抗をモデル化し、その影響を観察する。
# 
# 
# 問題設定：
# 
# ・温度 T が粒子のステップサイズに影響を与える。
# ・粒子の大きさ S が移動のしやすさに影響を与える。大きな粒子ほど移動が困難になると仮定する。
# ・2次元空間でのNステップのランダムウォークをシミュレートする。
# ・２種類の粒子を考える（S1, S2を設定する）
# 
# 実装手順：
# 
# 温度T と粒子の大きさ S 1, S2のパラメータを設定する。
# ステップサイズと移動抵抗を計算する関数を作成する。
# 温度と粒子の大きさを考慮したランダムウォークのシミュレーションを行い、結果を記録する。
# 
# 結果をプロットして視覚化する。
# 
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt

# パラメータの設定
N = 1000  # ステップ数
T = 300   # 温度
S1 = 0.5  # 粒子1の大きさ
S2 = 1.0  # 粒子2の大きさ

# 初期位置
x1, y1 = 0, 0
x2, y2 = 0, 0

# ステップサイズを計算する関数
def step_size(T, S):
    return np.sqrt(T) / S

# ランダムウォークの関数
def random_walk(N, T, S, x_init, y_init):
    x_positions = [x_init]
    y_positions = [y_init]
    for _ in range(N):
        step_direction = np.random.choice(['up', 'down', 'left', 'right'])
        step_length = step_size(T, S)
        
        if step_direction == 'up':
            y_init += step_length
        elif step_direction == 'down':
            y_init -= step_length
        elif step_direction == 'left':
            x_init -= step_length
        else:
            x_init += step_length

        x_positions.append(x_init)
        y_positions.append(y_init)
    
    return x_positions, y_positions

# 各粒子のランダムウォークを実行
x_positions1, y_positions1 = random_walk(N, T, S1, x1, y1)
x_positions2, y_positions2 = random_walk(N, T, S2, x2, y2)

# 結果のプロット
plt.figure(figsize=(10, 6))
plt.plot(x_positions1, y_positions1, color='blue', label='Particle 1 (Size = 0.5)')
plt.plot(x_positions2, y_positions2, color='red', label='Particle 2 (Size = 1.0)')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Random Walks of Two Particles with Different Sizes')
plt.legend()
plt.show()


