# -*- coding: utf-8 -*-
"""
演習：顕微鏡画像から円形の血球候補を見つける

学習する流れ
1. 画像を読み込む
2. グレースケール化とぼかし処理を行う
3. ハフ円変換で円を検出する
4. 検出位置を画像へ描く
5. 入力画像と結果画像を比較する

注意：これは画像処理の演習です。円形領域を「候補」として数えるだけで、
実際の血球数の測定や医療診断には使用できません。
"""

from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# 1. 画像ファイルの場所を作る
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
image_path = DATA_DIR / "blood.png"


# =============================================================================
# 2. 画像を読み込む（画像がなければ練習用画像を作る）
# =============================================================================

if image_path.exists():
    image_bgr = cv2.imread(str(image_path))
    if image_bgr is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")
else:
    print(f"画像がないため、練習用画像を作成します: {image_path}")
    rng = np.random.default_rng(42)
    image_bgr = np.full((500, 700, 3), 235, dtype=np.uint8)
    for _ in range(45):
        center_x = int(rng.integers(25, 675))
        center_y = int(rng.integers(25, 475))
        center = (center_x, center_y)
        radius = int(rng.integers(10, 19))
        cv2.circle(image_bgr, center, radius, (120, 120, 210), thickness=-1)
        inner_radius = max(2, radius - 4)
        cv2.circle(image_bgr, center, inner_radius, (190, 190, 240), thickness=2)


# =============================================================================
# 3. 円を検出しやすい画像へ変換する
# =============================================================================

# TODO: image_bgrをグレースケール画像へ変換してください（cv2.cvtColor, cv2.COLOR_BGR2GRAY）
gray_image = None

# TODO: gray_imageに軽くぼかしをかけてください（cv2.GaussianBlur、カーネルサイズ(9, 9)、sigmaX=1.5）
blurred_image = None


# =============================================================================
# 4. ハフ円変換で円を検出する
# =============================================================================

# TODO: cv2.HoughCircles()を使って円を検出してください
# ヒント：method=cv2.HOUGH_GRADIENT, dp=1.2, minDist=16,
#        param1=70, param2=22, minRadius=8, maxRadius=22
detected_circles = None


# =============================================================================
# 5. 検出結果を画像へ描く
# =============================================================================

result_image = image_bgr.copy()
candidate_count = 0

# TODO: detected_circlesがNoneでなければ、各円をresult_imageへ描き、
#       candidate_countに検出数を入れてください
# ヒント：np.uint16(np.around(detected_circles[0])) で整数座標へ変換し、
#        cv2.circle()で円周（緑）と中心点（赤）を描く


# =============================================================================
# 6. 個数を表示する
# =============================================================================

print(f"検出した円形の血球候補: {candidate_count}個")
print("注意：画像処理で見つけた候補であり、医療診断結果ではありません。")


# =============================================================================
# 7. 入力画像と結果画像を比較する
# =============================================================================

figure, axes = plt.subplots(1, 2, figsize=(12, 5))

input_image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

axes[0].imshow(input_image_rgb)
axes[0].set_title("Input image")

axes[1].imshow(result_image_rgb)
axes[1].set_title(f"Detected candidates: {candidate_count}")

for axis in axes:
    axis.axis("off")

figure.tight_layout()
plt.show()
