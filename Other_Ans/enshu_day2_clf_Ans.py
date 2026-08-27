# -*- coding: utf-8 -*-
"""
演習：分光スペクトルから飲料の種類を分類する（解答版）

【想定する場面】
飲料工場では、容器へ正しい製品が充填されているか確認する必要があります。
ここでは、製品ごとに異なる吸光スペクトルを使い、未知試料を
「Berry」「Green」「Orange」の3種類へ分類します。

分類とは、あらかじめ決められたグループのどれに属するかを予測する処理です。
今回はRandom Forestを使い、PCAと混同行列で結果を確認します。
"""

# matplotlib：スペクトルや分類結果をグラフで表示します。
import matplotlib.pyplot as plt

# NumPy：波長軸、スペクトル、乱数を扱います。
import numpy as np

# PCA：多数の波長データを2つの値へ要約し、散布図で見えるようにします。
from sklearn.decomposition import PCA

# Random Forest：複数の決定木の多数決でクラスを予測します。
from sklearn.ensemble import RandomForestClassifier

# 分類結果を評価する関数です。
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
)

# データを学習用とテスト用へ分割します。
from sklearn.model_selection import train_test_split


# =============================================================================
# 1. 模擬スペクトルを作る条件を設定する
# =============================================================================

# 乱数の種を42に固定し、毎回同じデータを再現します。
rng = np.random.default_rng(42)

# 400 nmから750 nmまでを1 nm間隔に近い351点で表します。
wavelengths = np.linspace(400, 750, 351)

# クラス番号と製品名の対応です。
class_names = ["Berry", "Green", "Orange"]

# 各製品で吸光度が最も高くなる代表的な波長です。
peak_centers = [460, 530, 615]

# スペクトルとクラス番号を保存する空リストを作ります。
spectra = []
labels = []


# =============================================================================
# 2. 3製品×50件の模擬スペクトルを作る
# =============================================================================

# enumerate()により、class_idには0、1、2が入り、peak_centerには
# それぞれ460、530、615が入ります。
for class_id, peak_center in enumerate(peak_centers):
    for _ in range(50):
        # 実物では試料ごとにピーク位置が少し変わることがあります。
        shifted_center = rng.normal(loc=peak_center, scale=5.0)

        # ガウス関数で、中心付近が高くなる滑らかなピークを作ります。
        exponent = -((wavelengths - shifted_center) ** 2) / (2 * 30.0 ** 2)
        ideal_spectrum = np.exp(exponent)

        # 平均0、標準偏差0.025の測定ノイズを加えます。
        noise = rng.normal(loc=0.0, scale=0.025, size=wavelengths.size)
        measured_spectrum = ideal_spectrum + noise

        spectra.append(measured_spectrum)
        labels.append(class_id)


# =============================================================================
# 3. 機械学習へ渡せるNumPy配列に変換する
# =============================================================================

# Xは特徴量です。1行が1試料、1列が1波長の吸光度になります。
X = np.asarray(spectra)

# yは正解ラベルです。0、1、2が製品種類を表します。
y = np.asarray(labels)

print("【作成した模擬データ】")
print(f"特徴量Xの形: {X.shape}（試料数, 波長数）")
print(f"正解ラベルyの形: {y.shape}")


# =============================================================================
# 4. 学習用データとテスト用データに分ける
# =============================================================================

# test_size=0.25により、25%を最終確認用のテストデータにします。
# stratify=yにより、3製品の割合を分割前後でほぼ同じに保ちます。
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

# n_estimators=200は、200本の決定木を作って多数決する指定です。
# random_state=42により、学習結果を再現できるようにします。
classifier = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
)

# fit()で学習データと正解ラベルの関係を学習します。
classifier.fit(X_train, y_train)

# predict()で、学習には使っていないテストデータを分類します。
predicted_labels = classifier.predict(X_test)


# =============================================================================
# 6. 分類結果を数値で評価する
# =============================================================================

# accuracyは、全テストデータのうち正しく分類できた割合です。
accuracy = accuracy_score(y_test, predicted_labels)
print(f"\n正解率: {accuracy:.3f}")

# classification_reportは、製品ごとのprecision、recall、F1を表示します。
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

# 元データは351波長あるため、そのままでは散布図にできません。
# PCAは情報をできるだけ保ちながら、ここでは2つの主成分へ要約します。
pca = PCA(n_components=2)
pca_scores = pca.fit_transform(X)

print("PCA第1・第2主成分の累積寄与率: "
      f"{pca.explained_variance_ratio_.sum():.3f}")


# =============================================================================
# 8. スペクトル、PCA、混同行列を可視化する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(16, 5))

# 左：各製品から1件ずつ代表スペクトルを表示します。
for class_id, class_name in enumerate(class_names):
    sample_index = np.where(y == class_id)[0][0]
    axes[0].plot(wavelengths, X[sample_index], label=class_name)

axes[0].set_title("Example spectra")
axes[0].set_xlabel("Wavelength (nm)")
axes[0].set_ylabel("Absorbance")
axes[0].legend()
axes[0].grid(alpha=0.25)

# 中央：PCAで2次元にした全試料を、正解クラス別に色分けします。
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

# 右：混同行列です。行が本当のクラス、列が予測クラスを表します。
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
