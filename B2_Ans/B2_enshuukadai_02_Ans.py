# -*- coding: utf-8 -*-
"""解答版：健康診断受診者の年齢分布を確認する。"""
import matplotlib.pyplot as plt
ages = [23,25,29,31,34,35,37,41,42,45,45,48,51,54,58,62,67,72]
plt.hist(ages, bins=[20,30,40,50,60,70,80], edgecolor="white", color="#54A24B")
plt.title("Age Distribution of Health-check Participants")
plt.xlabel("Age"); plt.ylabel("People"); plt.tight_layout(); plt.show()

