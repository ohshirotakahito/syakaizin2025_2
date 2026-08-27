# -*- coding: utf-8 -*-
"""解答版：3配送会社の所要時間分布を箱ひげ図で比較する。"""
import matplotlib.pyplot as plt
delivery_times = [[28,31,29,35,33,30,44], [24,26,25,27,29,26,28], [30,36,32,40,38,35,52]]
plt.boxplot(delivery_times, tick_labels=["A", "B", "C"], patch_artist=True)
plt.title("Delivery-time Distribution by Carrier")
plt.xlabel("Carrier"); plt.ylabel("Minutes"); plt.grid(axis="y", alpha=0.25)
plt.tight_layout(); plt.show()

