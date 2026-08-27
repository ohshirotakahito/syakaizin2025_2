# -*- coding: utf-8 -*-
"""
演習：手書き数字分類モデルを学習して保存する

【このプログラムの役割】
handwriting_recognition.pyで画像を認識する前に、0～9の数字を分類する
Random Forestを作ります。モデルの性能をテストデータで確認してから、
digits_random_forest.joblibとして保存します。

学習データとテストデータを分けないと、モデルが暗記したデータだけで
性能を評価することになり、未知画像への実力を公平に確認できません。
"""

from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
)
from sklearn.model_selection import train_test_split


# =============================================================================
# 1. モデルを保存する場所を作る
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
model_path = DATA_DIR / "digits_random_forest.joblib"


# =============================================================================
# 2. 手書き数字データを読み込んで確認する
# =============================================================================

digits = load_digits()
features = digits.data
targets = digits.target

print("【digitsデータセット】")
print(f"画像数: {len(digits.images)}")
print(f"画像1枚の形: {digits.images[0].shape}")
print(f"特徴量の形: {features.shape}（画像数, 画素数）")
print(f"画素値の範囲: {features.min():.0f}～{features.max():.0f}")


# =============================================================================
# 3. 学習用とテスト用へ分割する
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    features,
    targets,
    test_size=0.25,
    random_state=42,
    stratify=targets,
)

print(f"学習データ: {len(X_train)}件")
print(f"テストデータ: {len(X_test)}件")


# =============================================================================
# 4. Random Forestを学習する
# =============================================================================

# TODO: RandomForestClassifierを作成し、学習データで学習させてください
# ヒント： RandomForestClassifier(n_estimators=250, random_state=42)
#         classifier.fit(X_train, y_train)
classifier = None


# =============================================================================
# 5. 学習用・テスト用データを予測して評価する
# =============================================================================

# TODO: 学習データとテストデータそれぞれについて予測し、
#       正解率train_accuracy、test_accuracyを求めてください
train_predictions = None
test_predictions = None
train_accuracy = None
test_accuracy = None

print("\n【正解率】")
print(f"学習データ: {train_accuracy:.3f}")
print(f"テストデータ: {test_accuracy:.3f}")

print("\n【テストデータ：数字ごとの分類レポート】")
print(
    classification_report(
        y_test,
        test_predictions,
        target_names=[str(digit) for digit in range(10)],
        zero_division=0,
    )
)


# =============================================================================
# 6. 学習済みモデルを保存する
# =============================================================================

model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(classifier, model_path)
print(f"学習済みモデルの保存先: {model_path}")


# =============================================================================
# 7. モデルの結果を3種類の図で確認する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(16, 5))

sample_index = 0
sample_image = X_test[sample_index].reshape(8, 8)
actual_digit = int(y_test[sample_index])
predicted_digit = int(test_predictions[sample_index])

axes[0].imshow(sample_image, cmap="gray", vmin=0, vmax=16)
axes[0].set_title(f"Actual: {actual_digit} / Predicted: {predicted_digit}")
axes[0].axis("off")

ConfusionMatrixDisplay.from_predictions(
    y_test,
    test_predictions,
    cmap="Blues",
    ax=axes[1],
    colorbar=False,
)
axes[1].set_title("Test Confusion Matrix")

# TODO: classifier.feature_importances_を8×8に変換したimportance_imageを作り、
#       画素ごとの重要度を表示してください
importance_image = None
importance_plot = axes[2].imshow(importance_image, cmap="YlOrRd")
axes[2].set_title("Pixel Importance")
axes[2].axis("off")
figure.colorbar(importance_plot, ax=axes[2], fraction=0.046, pad=0.04)

figure.tight_layout()
plt.show()


# =============================================================================
# 結果を使うときの注意
# =============================================================================

print("\n注意：digitsは小さな8×8画像です。実際の写真とは条件が異なります。")
print("認識側でも背景、位置、サイズ、画素値を学習データに合わせる必要があります。")
