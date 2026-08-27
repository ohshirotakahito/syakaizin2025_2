# -*- coding: utf-8 -*-
"""
演習：ランダムウォークによる粒子の拡散のシミュレーション

目的：
・2次元空間での粒子のランダムウォークをシミュレートする。
・時間経過に伴う粒子の位置変化を観察し、拡散の概念を理解する。

※ このファイルはTODOを埋める前でも最後まで実行できます（粒子は原点から動きません）。
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

N = 1000
x, y = 0, 0

x_positions = [x]
y_positions = [y]

for _ in range(N):
    # TODO: rng.choice(['up', 'down', 'left', 'right'])でstepを決め、
    #       x, yをそれぞれの方向へ1動かしてください
    step = None

    x_positions.append(x)
    y_positions.append(y)

plt.plot(x_positions, y_positions)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Random Walk of a Particle in 2D Space')
plt.show()
