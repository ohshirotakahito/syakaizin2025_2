# -*- coding: utf-8 -*-
"""
演習：組織染色画像をグレースケール化しヒストグラムを作る

（課題）
画像（tex_image.png）は、細胞組織の染色画像です。カラー画像を
グレースケールに変換し、その後、画素値のヒストグラムを作成してください。

※ このファイルはTODOを埋める前でも最後まで実行できます
   （グレースケール画像の代わりに真っ黒な画像を使うため、ヒストグラムは1本だけになります）。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = DATA_DIR / "tex_image.png"

if image_path.exists():
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")
else:
    print(f"画像が見つからないため、演習用の模擬画像を作成します: {image_path}")
    rng = np.random.default_rng(42)
    image = np.full((300, 400, 3), 40, dtype=np.uint8)
    for _ in range(60):
        center = (int(rng.integers(10, 390)), int(rng.integers(10, 290)))
        radius = int(rng.integers(5, 15))
        color = tuple(int(c) for c in rng.integers(80, 220, size=3))
        cv2.circle(image, center, radius, color, thickness=-1)

# TODO: imageをグレースケール画像gray_imageへ変換してください
# ヒント： cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = np.zeros(image.shape[:2], dtype=np.uint8)  # 仮実装（真っ黒）

plt.hist(gray_image.ravel(), bins=256, range=[0, 256], color='black')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Histogram of Grayscale Image')
plt.show()
