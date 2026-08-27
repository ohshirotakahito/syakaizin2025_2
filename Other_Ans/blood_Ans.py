# -*- coding: utf-8 -*-
"""
演習：顕微鏡画像から円形の血球候補を見つける（解答版）

学習する流れ
1. 画像を読み込む
2. グレースケール化とぼかし処理を行う
3. ハフ円変換で円を検出する
4. 検出位置を画像へ描く
5. 入力画像と結果画像を比較する

注意：これは画像処理の演習です。円形領域を「候補」として数えるだけで、
実際の血球数の測定や医療診断には使用できません。
"""

# Path：OSによる区切り文字の違いを意識せず、ファイルの場所を扱います。
from pathlib import Path

# cv2：OpenCVの画像処理機能を使用します。
import cv2

# matplotlib：画像を画面に表示します。
import matplotlib.pyplot as plt

# NumPy：画像を構成する数値の配列を扱います。
import numpy as np


# =============================================================================
# 1. 画像ファイルの場所を作る
# =============================================================================

# __file__は、このblood_Ans.py自身の場所です。
# resolve()で絶対パスにし、parentを2回使ってプロジェクト直下へ移動します。
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 「/」演算子で、フォルダ名やファイル名を安全につなげられます。
DATA_DIR = PROJECT_ROOT / "data"
image_path = DATA_DIR / "blood.png"


# =============================================================================
# 2. 画像を読み込む（画像がなければ練習用画像を作る）
# =============================================================================

# exists()は、ファイルが存在するとTrue、存在しないとFalseを返します。
if image_path.exists():
    # imread()でカラー画像を読み込みます。
    # OpenCVのカラー画像はBGR（青・緑・赤）の順です。
    image_bgr = cv2.imread(str(image_path))

    # ファイルが壊れている場合などは、読み込み結果がNoneになります。
    if image_bgr is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")
else:
    print(f"画像がないため、練習用画像を作成します: {image_path}")

    # 42を固定すると、実行するたびに同じ乱数を再現できます。
    rng = np.random.default_rng(42)

    # 高さ500×幅700、3色の明るい背景画像を作ります。
    # uint8は、0～255の整数で色を表す画像用のデータ型です。
    image_bgr = np.full((500, 700, 3), 235, dtype=np.uint8)

    # 45個の円を描いて、血球に似た練習用画像を作ります。
    for _ in range(45):
        center_x = int(rng.integers(25, 675))
        center_y = int(rng.integers(25, 475))
        center = (center_x, center_y)
        radius = int(rng.integers(10, 19))

        # thickness=-1は、円の内側を塗りつぶす指定です。
        cv2.circle(image_bgr, center, radius, (120, 120, 210), thickness=-1)

        # 内側にも輪郭を描き、単純すぎない模擬画像にします。
        inner_radius = max(2, radius - 4)
        cv2.circle(image_bgr, center, inner_radius, (190, 190, 240), thickness=2)


# =============================================================================
# 3. 円を検出しやすい画像へ変換する
# =============================================================================

# 色情報をなくし、明るさだけを持つグレースケール画像へ変換します。
gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

# 少しぼかして、細かなノイズや輪郭のギザギザを減らします。
# (9, 9)は周囲を見る範囲、sigmaX=1.5はぼかしの強さです。
blurred_image = cv2.GaussianBlur(gray_image, (9, 9), sigmaX=1.5)


# =============================================================================
# 4. ハフ円変換で円を検出する
# =============================================================================

detected_circles = cv2.HoughCircles(
    blurred_image,                 # 円を探すグレースケール画像
    cv2.HOUGH_GRADIENT,            # 一般的なハフ円検出方法
    dp=1.2,                        # 検出計算に使う画像の解像度比
    minDist=16,                    # 円の中心同士に必要な最小距離
    param1=70,                     # 輪郭検出に使うしきい値
    param2=22,                     # 小さいほど多くの円を検出しやすい
    minRadius=8,                   # 探す円の最小半径
    maxRadius=22,                  # 探す円の最大半径
)


# =============================================================================
# 5. 検出結果を画像へ描く
# =============================================================================

# copy()により、入力画像を変更せず、複製した画像へ線を描けます。
result_image = image_bgr.copy()
candidate_count = 0

# 円が見つかると配列、見つからないとNoneが返ります。
if detected_circles is not None:
    # 検出座標は小数なので、四捨五入して画像用の整数へ変換します。
    rounded_circles = np.uint16(np.around(detected_circles[0]))
    candidate_count = len(rounded_circles)

    # 各円の中心x座標、中心y座標、半径を1組ずつ取り出します。
    for center_x, center_y, radius in rounded_circles:
        center = (int(center_x), int(center_y))

        # OpenCVはBGR順です。緑の円周と赤の中心点を描きます。
        cv2.circle(result_image, center, int(radius), (0, 180, 0), thickness=2)
        cv2.circle(result_image, center, 2, (0, 0, 255), thickness=2)


# =============================================================================
# 6. 個数を表示する
# =============================================================================

print(f"検出した円形の血球候補: {candidate_count}個")
print("注意：画像処理で見つけた候補であり、医療診断結果ではありません。")


# =============================================================================
# 7. 入力画像と結果画像を比較する
# =============================================================================

# 1行2列の表示領域を作ります。
figure, axes = plt.subplots(1, 2, figsize=(12, 5))

# OpenCVはBGR順、matplotlibはRGB順なので、表示前に変換します。
input_image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

axes[0].imshow(input_image_rgb)
axes[0].set_title("Input image")

axes[1].imshow(result_image_rgb)
axes[1].set_title(f"Detected candidates: {candidate_count}")

# 画像表示では座標軸が不要なので、左右両方で非表示にします。
for axis in axes:
    axis.axis("off")

# 文字や画像が重ならないように余白を調整してから表示します。
figure.tight_layout()
plt.show()
