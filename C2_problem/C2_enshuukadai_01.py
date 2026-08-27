# -*- coding: utf-8 -*-
"""
演習：ECサイトの購入画面を改善したA/Bテストの結果を分析する

【想定する場面】
ECサイトの購入画面を、従来版（A）とおすすめ商品を見やすくした改善版（B）の
2種類用意し、それぞれで実際に購入した顧客の注文金額を記録した。
改善版によって平均注文額が統計的に有意に変わったといえるかを検証する。

（課題）
1. A・B両群の平均・標準偏差を確認する。
2. Welchのt検定（分散が等しいと仮定しない検定）でp値を求める。
3. p値をもとに、統計的に有意な差があるかを判定する。
4. 箱ひげ図で両群の分布と平均を可視化する。

※ このファイルはTODOを埋める前でも最後まで実行できます。
   TODO部分は仮の値（t値=0.0, p値=1.0）になっているため、
   「有意差なし」という結論のまま表示されます。
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


group_a = np.array([
    2480, 3980, 5200, 1780, 6800, 3250, 4500, 2980, 8200, 2380,
    5600, 4100, 1950, 7300, 3480, 4750, 2650, 6100, 3850, 12800,
    2200, 4950, 3150, 7600, 2800, 5400, 3650, 1850, 8900, 4300,
])
group_b = np.array([
    3200, 4650, 5980, 2100, 7500, 3890, 5200, 3450, 9600, 2750,
    6400, 4880, 2300, 8100, 4200, 5500, 3100, 6900, 4450, 14600,
    2600, 5700, 3780, 8500, 3350, 6200, 4250, 2150, 9900, 5100,
])

# TODO: Welchのt検定（分散が等しいと仮定しない）を行い、t_statとp_valueを求めてください
# ヒント： stats.ttest_ind(group_a, group_b, equal_var=False)
t_stat, p_value = 0.0, 1.0

print("【ECサイト購入画面 A/Bテスト】")
print(f"A（従来画面）: 購入者数={len(group_a)}, 平均注文額={group_a.mean():,.0f}円, "
      f"標準偏差={group_a.std(ddof=1):,.0f}円")
print(f"B（改善画面）: 購入者数={len(group_b)}, 平均注文額={group_b.mean():,.0f}円, "
      f"標準偏差={group_b.std(ddof=1):,.0f}円")
print(f"平均注文額の増加: {group_b.mean() - group_a.mean():,.0f}円 "
      f"（{(group_b.mean() / group_a.mean() - 1) * 100:.1f}%）")
print(f"t値={t_stat:.3f}, p値={p_value:.5f}")

if p_value < 0.05:
    print("結論：改善版画面では、平均注文額が統計的に有意に変化しました。")
else:
    print("結論：購入画面による平均注文額の有意な差は確認できませんでした。")

fig, ax = plt.subplots(figsize=(9, 6))
groups = [group_a, group_b]
labels = ["A: Current checkout", "B: Improved checkout"]
colors = ["#4C78A8", "#F58518"]

box = ax.boxplot(groups, tick_labels=labels, patch_artist=True, widths=0.55)
for patch, color in zip(box["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.35)

rng = np.random.default_rng(42)
for position, (scores, color) in enumerate(zip(groups, colors), start=1):
    jitter = rng.normal(0, 0.045, len(scores))
    ax.scatter(position + jitter, scores, color=color, edgecolor="white",
               linewidth=0.7, s=55, alpha=0.9)
    ax.scatter(position, scores.mean(), marker="D", color="#222222",
               s=80, zorder=4)
    ax.text(position + 0.12, scores.mean(), f"Mean: JPY {scores.mean():,.0f}",
            va="center", fontsize=10)

ax.set_title(f"E-commerce A/B Test (Welch's t-test: p = {p_value:.4f})")
ax.set_ylabel("Order value (JPY)")
ax.yaxis.set_major_formatter(lambda value, position: f"{value:,.0f}")
ax.set_ylim(0, 16000)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
plt.show()
