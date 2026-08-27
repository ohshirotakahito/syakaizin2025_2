# -*- coding: utf-8 -*-
"""解答版：倉庫床面の高さを3Dサーフェスで点検する。"""
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(-5,5,60); y = np.linspace(-5,5,60)
X, Y = np.meshgrid(x, y)
Z = 0.03 * X + 0.02 * Y + 0.18 * np.exp(-(X**2 + Y**2) / 4)
fig = plt.figure(figsize=(9,6)); ax = fig.add_subplot(111, projection="3d")
surface = ax.plot_surface(X, Y, Z, cmap="viridis")
ax.set(title="Warehouse Floor Height Survey", xlabel="X (m)", ylabel="Y (m)", zlabel="Height (m)")
fig.colorbar(surface, ax=ax, shrink=0.6); plt.tight_layout(); plt.show()

