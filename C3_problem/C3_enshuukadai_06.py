# -*- coding: utf-8 -*-
"""
演習：温度と粒子の大きさに依存するランダムウォークのシミュレーション

（5番を踏まえた拡張）

目的：
・温度と粒子の大きさがランダムウォークの動きにどのように影響するかを理解する。
・粒子の大きさに応じて移動抵抗をモデル化し、その影響を観察する。

※ このファイルはTODOを埋める前でも最後まで実行できます（粒子は原点から動きません）。
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

N = 1000
T = 300
S1 = 0.5
S2 = 1.0

x1, y1 = 0, 0
x2, y2 = 0, 0


def step_size(T, S):
    """温度Tと粒子の大きさSから、1歩あたりの移動距離を計算する。"""
    # TODO: sqrt(T) / S を返してください
    # ヒント： return np.sqrt(T) / S
    return 0.0


def random_walk(N, T, S, x_init, y_init):
    """指定した温度T・大きさSの粒子について、Nステップのランダムウォークを行う。"""
    x_positions = [x_init]
    y_positions = [y_init]
    step_length = step_size(T, S)

    for _ in range(N):
        step_direction = rng.choice(['up', 'down', 'left', 'right'])

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


x_positions1, y_positions1 = random_walk(N, T, S1, x1, y1)
x_positions2, y_positions2 = random_walk(N, T, S2, x2, y2)

plt.figure(figsize=(10, 6))
plt.plot(x_positions1, y_positions1, color='blue', label='Particle 1 (Size = 0.5)')
plt.plot(x_positions2, y_positions2, color='red', label='Particle 2 (Size = 1.0)')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Random Walks of Two Particles with Different Sizes')
plt.legend()
plt.show()
