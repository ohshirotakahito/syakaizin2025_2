# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""2つの学習方法によるテスト得点の差をt検定で比較する。"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# 同じ難易度の試験を受けた学生の得点（100点満点）
group1 = np.array([62, 68, 71, 65, 74, 69, 77, 58, 72, 66,
                   70, 64, 75, 61, 73, 67, 69, 76, 63, 71])
group2 = np.array([70, 75, 78, 72, 81, 74, 85, 68, 79, 73,
                   77, 71, 82, 69, 80, 76, 74, 83, 72, 78])

# 分散が等しいと仮定しないWelchのt検定
t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

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

# 箱ひげ図に、学生ごとの得点と平均値を重ねて表示
fig, ax = plt.subplots(figsize=(9, 6))
groups = [group1, group2]
labels = ["Traditional class", "Class with video materials"]
colors = ["#4C78A8", "#F58518"]

box = ax.boxplot(groups, tick_labels=labels, patch_artist=True, widths=0.55)
for patch, color in zip(box["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.35)

# 個々の点が重ならないよう、小さな横方向のずれを加える
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
