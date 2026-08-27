# -*- coding: utf-8 -*-
"""
演習：2つの学習方法によるテスト得点の差をt検定で比較する

【想定する場面】
同じ難易度の試験を受けた学生を、従来型の授業を受けたグループと、
動画教材を併用した授業を受けたグループに分け、試験の得点を比較する。
動画教材によって得点が統計的に有意に変わったといえるかを検証する。

（課題）
1. 2グループの人数・平均・標準偏差を確認する。
2. Welchのt検定でp値を求める。
3. p値をもとに、統計的に有意な差があるかを判定する。
4. 箱ひげ図で両グループの分布と平均を可視化する。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

group1 = np.array([62, 68, 71, 65, 74, 69, 77, 58, 72, 66,
                   70, 64, 75, 61, 73, 67, 69, 76, 63, 71])
group2 = np.array([70, 75, 78, 72, 81, 74, 85, 68, 79, 73,
                   77, 71, 82, 69, 80, 76, 74, 83, 72, 78])

# TODO: Welchのt検定を行い、t_statとp_valueを求めてください
# ヒント： stats.ttest_ind(group1, group2, equal_var=False)
t_stat, p_value = 0.0, 1.0

print("【テスト得点の比較】")
print(f"従来型授業       : 人数={len(group1)}, 平均={group1.mean():.1f}点, "
      f"標準偏差={group1.std(ddof=1):.1f}点")
print(f"動画教材あり授業 : 人数={len(group2)}, 平均={group2.mean():.1f}点, "
      f"標準偏差={group2.std(ddof=1):.1f}点")
print(f"平均点の差       : {group2.mean() - group1.mean():.1f}点")
print(f"t値={t_stat:.3f}, p値={p_value:.5f}")

if p_value < 0.05:
    print("結論：2つの授業の平均点には、統計的に有意な差があります。")
else:
    print("結論：2つの授業の平均点に、統計的に有意な差は確認できません。")

fig, ax = plt.subplots(figsize=(9, 6))
groups = [group1, group2]
labels = ["Traditional class", "Class with video materials"]
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
    ax.text(position + 0.12, scores.mean(), f"Mean: {scores.mean():.1f}",
            va="center", fontsize=10)

ax.set_title(f"Comparison of Test Scores (Welch's t-test: p = {p_value:.4f})")
ax.set_ylabel("Test score (out of 100)")
ax.set_ylim(50, 90)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
plt.show()
