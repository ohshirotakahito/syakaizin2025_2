# -*- coding: utf-8 -*-
"""解答版：商品寸法データの関係をSeabornで一覧表示する。"""
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# 内蔵データを商品試作品の寸法測定例として利用し、ネット接続を不要にします。
data = load_iris(as_frame=True).frame
data["product_type"] = data.pop("target").map({0:"A", 1:"B", 2:"C"})
sns.pairplot(data, hue="product_type", corner=True, plot_kws={"alpha":0.6})
plt.show()

