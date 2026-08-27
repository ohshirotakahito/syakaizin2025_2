# -*- coding: utf-8 -*-
"""
演習：蛍光顕微鏡画像を色でセグメンテーションする

（課題）
画像（cell_microscope_image.png）は、蛍光顕微鏡で撮影された細胞の
イメージです。核、細胞内小胞体、細胞骨格がそれぞれ異なる色で
染色されています（核=明るい青、細胞内小胞体=明るい緑、細胞骨格=鮮やかな赤）。
画像の色に基づいてセグメンテーションを行い、異なる色を持つ領域を
異なる色でラベリングして表示してください。核、細胞内小胞体、細胞骨格の
割合を計算してください。

※ このファイルはTODOを埋める前でも最後まで実行できます
   （マスクがすべて0になるため、割合は0%、ラベル画像は元画像のままになります）。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = DATA_DIR / "cell_microscope_image.png"

if image_path.exists():
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
else:
    print(f"画像が見つからないため、演習用の模擬画像を作成します: {image_path}")
    rng = np.random.default_rng(42)
    image_rgb = np.full((400, 400, 3), 15, dtype=np.uint8)

    for _ in range(8):
        center = (int(rng.integers(30, 370)), int(rng.integers(30, 370)))
        cv2.circle(image_rgb, center, int(rng.integers(15, 30)), (0, 0, 220), -1)
    for _ in range(12):
        center = (int(rng.integers(30, 370)), int(rng.integers(30, 370)))
        cv2.circle(image_rgb, center, int(rng.integers(8, 18)), (0, 200, 0), -1)
    for _ in range(30):
        pt1 = (int(rng.integers(0, 400)), int(rng.integers(0, 400)))
        pt2 = (int(rng.integers(0, 400)), int(rng.integers(0, 400)))
        cv2.line(image_rgb, pt1, pt2, (220, 0, 0), 2)

plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.axis('off')
plt.title('Original Image')

# TODO: 青（核）の領域を抽出するマスクmask_blueを作ってください
# ヒント： cv2.inRange(image_rgb, (0, 0, 100), (100, 100, 255))
mask_blue = np.zeros(image_rgb.shape[:2], dtype=np.uint8)  # 仮実装

# TODO: 緑（細胞内小胞体）の領域を抽出するマスクmask_greenを作ってください
# ヒント： cv2.inRange(image_rgb, (0, 100, 0), (100, 255, 100))
mask_green = np.zeros(image_rgb.shape[:2], dtype=np.uint8)  # 仮実装

# TODO: 赤（細胞骨格）の領域を抽出するマスクmask_redを作ってください
# ヒント： cv2.inRange(image_rgb, (100, 0, 0), (255, 100, 100))
mask_red = np.zeros(image_rgb.shape[:2], dtype=np.uint8)  # 仮実装

total_pixels = image_rgb.shape[0] * image_rgb.shape[1]
blue_ratio = (mask_blue > 0).sum() / total_pixels
green_ratio = (mask_green > 0).sum() / total_pixels
red_ratio = (mask_red > 0).sum() / total_pixels

print(f"核（青）の面積割合: {blue_ratio:.1%}")
print(f"細胞内小胞体（緑）の面積割合: {green_ratio:.1%}")
print(f"細胞骨格（赤）の面積割合: {red_ratio:.1%}")

labeled_image = image_rgb.copy()
labeled_image[mask_blue > 0] = [0, 0, 255]
labeled_image[mask_green > 0] = [0, 255, 0]
labeled_image[mask_red > 0] = [255, 0, 0]

plt.figure(figsize=(10, 10))
plt.imshow(labeled_image)
plt.axis('off')
plt.title('Labeled Image')
plt.show()
