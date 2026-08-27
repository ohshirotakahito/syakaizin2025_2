# -*- coding: utf-8 -*-
"""
演習：顕微鏡画像を二値化し、粒子候補を計数する

【想定する場面】
顕微鏡画像をOtsu法で二値化し、モルフォロジー処理でノイズを除去したうえで、
連結成分解析により粒子候補の数と面積を求める。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
import cv2
import matplotlib.pyplot as plt
import numpy as np

image_path = Path(DATA_DIR / "particle.png")
if image_path.exists():
    gray = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
else:
    rng = np.random.default_rng(7)
    gray = np.full((500, 700), 25, dtype=np.uint8)
    for _ in range(70):
        center = (int(rng.integers(15, 685)), int(rng.integers(15, 485)))
        radius = int(rng.integers(4, 12))
        cv2.circle(gray, center, radius, int(rng.integers(170, 245)), -1)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

# TODO: Otsu法で画像ごとにしきい値を決め、二値画像binaryを作ってください
# ヒント： cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#         戻り値は (threshold_value, binary) の2つ
threshold_value = None
binary = None

# TODO: 3x3のカーネルでモルフォロジー膨張・収縮（オープニング）を行い、
#       小さなノイズを除去したcleanedを作ってください
# ヒント： kernel = np.ones((3, 3), np.uint8)
#         cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
kernel = np.ones((3, 3), np.uint8)
cleaned = None

# TODO: 連結成分を測定し、面積が35ピクセル以上の候補だけをvalid_labelsとしてください
# ヒント： number, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned)
#         stats[label, cv2.CC_STAT_AREA] で各成分の面積が得られる
number, labels, stats, centroids = None, None, None, None
valid_labels = []

overlay = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
for label in valid_labels:
    x, y, width, height, area = stats[label]
    cv2.rectangle(overlay, (x, y), (x + width, y + height), (255, 60, 60), 1)

areas = [stats[label, cv2.CC_STAT_AREA] for label in valid_labels]
print(f"Otsuしきい値: {threshold_value:.1f}")
print(f"粒子候補数: {len(valid_labels)}")
if areas:
    print(f"平均投影面積: {np.mean(areas):.1f} pixel")

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
axes[0].imshow(gray, cmap="gray")
axes[0].set_title("Input")
axes[1].imshow(cleaned, cmap="gray")
axes[1].set_title("Binary / cleaned")
axes[2].imshow(overlay)
axes[2].set_title(f"Particles: {len(valid_labels)}")
for ax in axes:
    ax.axis("off")
fig.tight_layout()
plt.show()

print("重なった粒子は1個として数える場合があり、必要ならwatershed分離を検討します。")
