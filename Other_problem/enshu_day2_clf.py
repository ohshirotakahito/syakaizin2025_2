# -*- coding: utf-8 -*-
"""
演習：分光スペクトルから飲料の種類を分類する

【想定する場面】
飲料工場では、容器へ正しい製品が充填されているか確認する必要があります。
ここでは、製品ごとに異なる吸光スペクトルを使い、未知試料を
「Berry」「Green」「Orange」の3種類へ分類します。

分類とは、あらかじめ決められたグループのどれに属するかを予測する処理です。
今回はRandom Forestを使い、PCAと混同行列で結果を確認します。
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
)
from sklearn.model_selection import train_test_split


# =============================================================================
# 1. 模擬スペクトルを作る条件を設定する
# =============================================================================

rng = np.random.default_rng(42)
wavelengths = np.linspace(400, 750, 351)
class_names = ["Berry", "Green", "Orange"]
peak_centers = [460, 530, 615]

spectra = []
labels = []


# =============================================================================
# 2. 3製品×50件の模擬スペクトルを作る
# =============================================================================

for class_id, peak_center in enumerate(peak_centers):
    for _ in range(50):
        shifted_center = rng.normal(loc=peak_center, scale=5.0)
        exponent = -((wavelengths - shifted_center) ** 2) / (2 * 30.0 ** 2)
        ideal_spectrum = np.exp(exponent)
        noise = rng.normal(loc=0.0, scale=0.025, size=wavelengths.size)
        measured_spectrum = ideal_spectrum + noise

        spectra.append(measured_spectrum)
        labels.append(class_id)


# =============================================================================
# 3. 機械学習へ渡せるNumPy配列に変換する
# =============================================================================

X = np.asarray(spectra)
y = np.asarray(labels)

print("【作成した模擬データ】")
print(f"特徴量Xの形: {X.shape}（試料数, 波長数）")
print(f"正解ラベルyの形: {y.shape}")


# =============================================================================
# 4. 学習用データとテスト用データに分ける
# =============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

print(f"学習データ: {len(X_train)}件")
print(f"テストデータ: {len(X_test)}件")


# =============================================================================
# 5. Random Forestを学習する
# =============================================================================

# TODO: RandomForestClassifierを作成してください
# ヒント： n_estimators=200, random_state=42
classifier = None

# TODO: classifier.fit()で学習し、classifier.predict()でX_testを分類してください
predicted_labels = None


# =============================================================================
# 6. 分類結果を数値で評価する
# =============================================================================

accuracy = accuracy_score(y_test, predicted_labels)
print(f"\n正解率: {accuracy:.3f}")

print("\n【製品ごとの分類レポート】")
print(
    classification_report(
        y_test,
        predicted_labels,
        target_names=class_names,
        zero_division=0,
    )
)


# =============================================================================
# 7. PCAでスペクトル全体の分布を2次元に要約する
# =============================================================================

# TODO: PCA(n_components=2)を作り、Xをpca_scoresへ要約してください
pca = None
pca_scores = None

print("PCA第1・第2主成分の累積寄与率: "
      f"{pca.explained_variance_ratio_.sum():.3f}")


# =============================================================================
# 8. スペクトル、PCA、混同行列を可視化する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(16, 5))

for class_id, class_name in enumerate(class_names):
    sample_index = np.where(y == class_id)[0][0]
    axes[0].plot(wavelengths, X[sample_index], label=class_name)

axes[0].set_title("Example spectra")
axes[0].set_xlabel("Wavelength (nm)")
axes[0].set_ylabel("Absorbance")
axes[0].legend()
axes[0].grid(alpha=0.25)

for class_id, class_name in enumerate(class_names):
    class_mask = y == class_id
    axes[1].scatter(
        pca_scores[class_mask, 0],
        pca_scores[class_mask, 1],
        label=class_name,
        alpha=0.75,
    )

axes[1].set_title("PCA overview")
axes[1].set_xlabel("Principal component 1")
axes[1].set_ylabel("Principal component 2")
axes[1].legend()
axes[1].grid(alpha=0.25)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    predicted_labels,
    display_labels=class_names,
    cmap="Blues",
    ax=axes[2],
    colorbar=False,
)
axes[2].set_title("Test confusion matrix")

figure.tight_layout()
plt.show()


# =============================================================================
# 結果を使うときの注意
# =============================================================================

print("注意：この結果は人工的に作った模擬データでの性能です。")
print("実際の運用前には、別ロット・別測定日・装置差を含む実データで検証します。")
