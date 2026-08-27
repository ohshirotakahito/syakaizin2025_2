# -*- coding: utf-8 -*-
"""
演習：手書き数字分類モデルを学習して保存する（解答版）

【このプログラムの役割】
handwriting_recognition_Ans.pyで画像を認識する前に、0～9の数字を分類する
Random Forestを作ります。モデルの性能をテストデータで確認してから、
digits_random_forest.joblibとして保存します。

学習データとテストデータを分けないと、モデルが暗記したデータだけで
性能を評価することになり、未知画像への実力を公平に確認できません。
"""

# Path：モデルの保存場所を、実行位置に依存せず作ります。
from pathlib import Path

# joblib：学習済みモデルをファイルへ保存します。
import joblib

# matplotlib：数字画像、混同行列、重要度を表示します。
import matplotlib.pyplot as plt

# NumPy：予測結果や画像位置の配列を扱います。
import numpy as np

# load_digits：scikit-learn付属の8×8手書き数字データです。
from sklearn.datasets import load_digits

# Random Forest：複数の決定木の多数決で数字を分類します。
from sklearn.ensemble import RandomForestClassifier

# 分類モデルを評価するための機能です。
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
)

# 学習用データとテスト用データへ分けます。
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

# digits.images：8×8の画像
# digits.data  ：画像を64個の数値へ横一列にした特徴量
# digits.target：画像に書かれた本当の数字
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

# 全データの25%をテスト専用に残します。
# stratify=targetsにより、0～9の割合を分割前後でほぼ同じに保ちます。
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

# n_estimators=250は、250本の決定木を作って多数決する指定です。
# random_state=42により、実行するたびに同じ学習結果を再現できます。
classifier = RandomForestClassifier(
    n_estimators=250,
    random_state=42,
)

# fit()へ特徴量と正解を渡し、画素と数字の関係を学習します。
classifier.fit(X_train, y_train)


# =============================================================================
# 5. 学習用・テスト用データを予測して評価する
# =============================================================================

train_predictions = classifier.predict(X_train)
test_predictions = classifier.predict(X_test)

train_accuracy = accuracy_score(y_train, train_predictions)
test_accuracy = accuracy_score(y_test, test_predictions)

print("\n【正解率】")
print(f"学習データ: {train_accuracy:.3f}")
print(f"テストデータ: {test_accuracy:.3f}")

# 学習正解率だけが高く、テスト正解率が低い場合は過学習が疑われます。
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

# parents=Trueにより途中のフォルダも作り、exist_ok=Trueで既存でもエラーにしません。
model_path.parent.mkdir(parents=True, exist_ok=True)

# dump()で、学習済みclassifierを1つのファイルへ保存します。
joblib.dump(classifier, model_path)
print(f"学習済みモデルの保存先: {model_path}")


# =============================================================================
# 7. モデルの結果を3種類の図で確認する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(16, 5))

# 左：テストデータの最初の数字と、モデルの予測を表示します。
sample_index = 0
sample_image = X_test[sample_index].reshape(8, 8)
actual_digit = int(y_test[sample_index])
predicted_digit = int(test_predictions[sample_index])

axes[0].imshow(sample_image, cmap="gray", vmin=0, vmax=16)
axes[0].set_title(f"Actual: {actual_digit} / Predicted: {predicted_digit}")
axes[0].axis("off")

# 中央：混同行列です。行が本当の数字、列が予測した数字です。
ConfusionMatrixDisplay.from_predictions(
    y_test,
    test_predictions,
    cmap="Blues",
    ax=axes[1],
    colorbar=False,
)
axes[1].set_title("Test Confusion Matrix")

# 右：64画素それぞれが分類へどの程度使われたかを表示します。
# feature_importances_を8×8へ戻すと、画像上の位置として見られます。
importance_image = classifier.feature_importances_.reshape(8, 8)
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
