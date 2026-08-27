# -*- coding: utf-8 -*-
"""
演習：手書き数字画像を0～9へ分類する

【想定する場面】
紙に書かれた数字を画像から読み取り、入力作業を補助する仕組みを考えます。
学習済みRandom Forestへ画像を渡すには、学習時と同じ8×8画素、
背景0・文字16程度の形式へ前処理する必要があります。

このプログラムは学習用です。確信度が高くても必ず正しいとは限らないため、
重要な番号の自動入力には人による確認が必要です。
"""

from pathlib import Path
import cv2
import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier


# =============================================================================
# 1. モデルファイルと画像ファイルの場所を作る
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

model_path = DATA_DIR / "digits_random_forest.joblib"
image_path = DATA_DIR / "tegaki.png"


# =============================================================================
# 2. 学習済みモデルを読み込む
# =============================================================================

if model_path.exists():
    classifier = joblib.load(model_path)
    print(f"学習済みモデルを読み込みました: {model_path.name}")
else:
    print("モデルがないため、digitsデータで新しいモデルを学習します。")
    digits = load_digits()

    classifier = RandomForestClassifier(
        n_estimators=250,
        random_state=42,
    )
    classifier.fit(digits.data, digits.target)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(classifier, model_path)


# =============================================================================
# 3. 認識する画像を読み込む
# =============================================================================

if image_path.exists():
    input_image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if input_image is None:
        raise ValueError(f"画像を読み込めませんでした: {image_path}")
    print(f"手書き画像を読み込みました: {image_path.name}")
else:
    digits = load_digits()
    sample_number = 42
    input_image = np.uint8(digits.images[sample_number] / 16.0 * 255)
    print(f"画像がないため、digitsのサンプル{sample_number}を使用します。")
    print(f"サンプルの本当の数字: {digits.target[sample_number]}")


# =============================================================================
# 4. 画像を学習データと同じ形式へ前処理する
# =============================================================================

# 白い紙に黒い文字がある場合、平均画素値は明るい値になります。
# digitsデータは黒背景に明るい文字なので、その場合は白黒を反転します。
working_image = input_image.copy()
if working_image.mean() > 127:
    working_image = 255 - working_image

# TODO: 30より明るい部分を文字候補として、0または255の二値画像binary_imageにしてください
# ヒント： cv2.threshold(working_image, 30, 255, cv2.THRESH_BINARY)
binary_image = None

# TODO: cv2.findNonZero()で、文字候補がある画素の座標を探してください
# 見つからない場合は raise ValueError("画像から数字らしい線を見つけられませんでした。")
non_zero_points = None

# TODO: cv2.boundingRect()で、文字候補全体を囲む最小の長方形(x, y, width, height)を求め、
#       working_imageから切り出してcropped_imageにしてください
x, y, width, height = None, None, None, None
cropped_image = None

# 縦横比を保つため、正方形の黒いキャンバス中央へ切出し画像を置きます。
side_length = max(width, height) + 4
square_image = np.zeros((side_length, side_length), dtype=np.uint8)
offset_x = (side_length - width) // 2
offset_y = (side_length - height) // 2
square_image[offset_y:offset_y + height, offset_x:offset_x + width] = cropped_image

# TODO: square_imageを学習データと同じ8×8画素へ縮小し、
#       0～16の範囲(model_image)へ変換してください
# ヒント： resized_image = cv2.resize(square_image, (8, 8), interpolation=cv2.INTER_AREA)
#         model_image = resized_image.astype(float) / 255.0 * 16.0
model_image = None


# =============================================================================
# 5. 数字を予測する
# =============================================================================

model_input = model_image.reshape(1, -1)

# TODO: classifier.predict_proba()で0～9それぞれの予測確率を求め、
#       最も確率の高い数字predicted_digitとその確信度confidenceを求めてください
# ヒント： probabilities = classifier.predict_proba(model_input)[0]
#         predicted_digit = int(np.argmax(probabilities))
#         confidence = float(probabilities[predicted_digit])
probabilities = None
predicted_digit = None
confidence = None

print(f"\n予測数字: {predicted_digit}")
print(f"予測上の確信度: {confidence:.1%}")

top_three = np.argsort(probabilities)[::-1][:3]
print("上位3候補:")
for digit in top_three:
    print(f"  {digit}: {probabilities[digit]:.1%}")

if confidence < 0.70:
    print("確信度が70%未満のため、人による確認を推奨します。")


# =============================================================================
# 6. 入力、前処理、予測確率を可視化する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(13, 4))

axes[0].imshow(input_image, cmap="gray")
axes[0].set_title("Input image")
axes[0].axis("off")

axes[1].imshow(model_image, cmap="gray", vmin=0, vmax=16)
axes[1].set_title("Model input (8 x 8)")
axes[1].axis("off")

bar_colors = ["crimson" if digit == predicted_digit else "steelblue"
              for digit in range(10)]
axes[2].bar(range(10), probabilities, color=bar_colors)
axes[2].set_title(f"Prediction: {predicted_digit} ({confidence:.1%})")
axes[2].set_xlabel("Digit")
axes[2].set_ylabel("Predicted probability")
axes[2].set_xticks(range(10))
axes[2].set_ylim(0, 1)
axes[2].grid(axis="y", alpha=0.25)

figure.tight_layout()
plt.show()


# =============================================================================
# 結果を使うときの注意
# =============================================================================

print("\n注意：表示した確信度はモデルの出力であり、正解の保証ではありません。")
print("文字の位置、太さ、傾き、画像の明るさが学習データと違うと誤認識します。")
