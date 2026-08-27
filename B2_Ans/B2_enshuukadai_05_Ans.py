# -*- coding: utf-8 -*-
"""解答版：広告費と問い合わせ数の関係を散布図で確認する。"""
import matplotlib.pyplot as plt
ad_spend = [10,15,18,22,28,35,40,48,55,62]
inquiries = [22,25,31,29,40,48,46,61,65,70]
plt.scatter(ad_spend, inquiries, s=70, color="#4C78A8")
plt.title("Advertising Spend and Inquiries")
plt.xlabel("Ad spend (10,000 JPY)"); plt.ylabel("Inquiries")
plt.grid(alpha=0.25); plt.tight_layout(); plt.show()

