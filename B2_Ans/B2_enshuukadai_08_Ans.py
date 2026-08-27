# -*- coding: utf-8 -*-
"""解答版：キャンペーン開始日を売上グラフへ注釈する。"""
import matplotlib.pyplot as plt
days = [1,2,3,4,5,6,7]; sales = [82,85,80,118,130,126,140]
plt.plot(days, sales, marker="o", label="Daily sales")
plt.annotate("Campaign started", xy=(4,118), xytext=(1.8,135),
             arrowprops={"arrowstyle":"->", "color":"red"})
plt.xlabel("Day"); plt.ylabel("Units"); plt.title("Campaign Effect")
plt.legend(); plt.grid(alpha=0.25); plt.tight_layout(); plt.show()

