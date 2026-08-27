# -*- coding: utf-8 -*-
"""解答版：倉庫在庫の推移を読みやすくカスタマイズする。"""
import matplotlib.pyplot as plt
days = list(range(1, 8)); stock = [320,285,260,210,175,140,95]
plt.plot(days, stock, marker="o", linewidth=2, color="#E45756")
plt.axhline(120, linestyle="--", color="gray", label="Reorder point")
plt.title("Warehouse Inventory"); plt.xlabel("Day"); plt.ylabel("Units")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout(); plt.show()

