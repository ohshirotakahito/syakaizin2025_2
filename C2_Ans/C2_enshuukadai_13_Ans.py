from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：処理の結果だけでなく、前提・指標・業務上の意味も確認します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
#１３．基本的な画像処理:
#画像（tex.png）は，細胞組織の染色画像となります．カラー画像をグレースケールに変換し、その後、ヒストグラムを作成してください。

import cv2
import matplotlib.pyplot as plt  # matplotlib.pyplotを正しくインポートする

# 画像の読み込み
image = cv2.imread(DATA_DIR / "tex_image.png")

# 元の画像を表示
# cv2.imshow('Original Image', image)
# cv2.waitKey(0)  # キーボード入力があるまでウィンドウを表示

# カラー画像をグレースケールに変換
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# グレースケール画像を表示
# cv2.imshow('Grayscale Image', gray_image)
# cv2.waitKey(0)  # キーボード入力があるまでウィンドウを表示

# ヒストグラムの作成
plt.hist(gray_image.ravel(), bins=256, range=[0, 256], color='black')  # fcとecの代わりにcolorを使用
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Histogram of Grayscale Image')
plt.show()




