# -*- coding: utf-8 -*-
"""解答版：新商品の週次売上推移を折れ線グラフで確認する。"""
import matplotlib.pyplot as plt
weeks = [1, 2, 3, 4, 5, 6]
sales = [120, 155, 148, 190, 225, 210]
plt.plot(weeks, sales, marker="o", color="#4C78A8")
plt.title("Weekly Sales after Product Launch")
plt.xlabel("Week"); plt.ylabel("Units sold"); plt.grid(alpha=0.3)
plt.tight_layout(); plt.show()

