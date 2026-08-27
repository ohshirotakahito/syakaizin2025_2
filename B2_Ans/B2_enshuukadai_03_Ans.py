# -*- coding: utf-8 -*-
"""解答版：問い合わせ理由別の件数を棒グラフで比較する。"""
import matplotlib.pyplot as plt
categories = ["Delivery", "Payment", "Product", "Account"]
counts = [42, 18, 31, 12]
bars = plt.bar(categories, counts, color="#F58518")
plt.bar_label(bars); plt.title("Customer Inquiries by Category")
plt.ylabel("Cases"); plt.tight_layout(); plt.show()

