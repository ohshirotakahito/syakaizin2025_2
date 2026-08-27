# -*- coding: utf-8 -*-
"""解答版：月次売上の実績と目標を同じ図で比較する。"""
import matplotlib.pyplot as plt
months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
actual = [420,450,470,510,495,540]
target = [430,450,470,490,510,530]
plt.plot(months, actual, marker="o", label="Actual")
plt.plot(months, target, marker="s", linestyle="--", label="Target")
plt.title("Monthly Sales: Actual vs Target"); plt.ylabel("10,000 JPY")
plt.legend(); plt.grid(alpha=0.25); plt.tight_layout(); plt.show()

