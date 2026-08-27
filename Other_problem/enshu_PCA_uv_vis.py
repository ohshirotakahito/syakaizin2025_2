# -*- coding: utf-8 -*-
"""
演習：UV-VisスペクトルをPCAで要約し、製造ロットを比較する

【想定する場面】
飲料工場で同じ製品を3つの製造ロットに分けて生産しました。UV-Vis測定では、
1試料につき451波長の吸光度が得られます。451個の数値をそのまま比較する
代わりに、PCA（主成分分析）で2個の主成分へ要約します。

PCAは正解ラベルを使わず、データのばらつきが大きい方向を見つける
「教師なし学習」です。スコアとローディングは役割が異なります。
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 模擬UV-Visスペクトルを作る条件
# =============================================================================

rng = np.random.default_rng(42)
wavelengths = np.linspace(350, 800, 451)
lot_names = ["Lot A", "Lot B", "Lot C"]
peak_centers = [470, 520, 575]

spectra = []
lot_labels = []


# =============================================================================
# 2. 3ロット×18試料の模擬スペクトルを作る
# =============================================================================

for lot_id, peak_center in enumerate(peak_centers):
    for _ in range(18):
        shifted_center = rng.normal(loc=peak_center, scale=3.0)
        exponent = -((wavelengths - shifted_center) ** 2) / (2 * 32.0 ** 2)
        absorption_peak = np.exp(exponent)
        noise = rng.normal(loc=0.0, scale=0.015, size=wavelengths.size)
        measured_spectrum = 0.04 + absorption_peak + noise

        spectra.append(measured_spectrum)
        lot_labels.append(lot_id)


# =============================================================================
# 3. NumPy配列へ変換し、データの形を確認する
# =============================================================================

X = np.asarray(spectra)
labels = np.asarray(lot_labels)

print("【UV-Vis模擬データ】")
print(f"Xの形: {X.shape}（試料数, 波長数）")
print(f"ロット数: {len(lot_names)}")


# =============================================================================
# 4. 波長ごとに標準化する
# =============================================================================

scaler = StandardScaler()
standardized_X = scaler.fit_transform(X)

print("標準化後の全列平均の絶対最大値: "
      f"{np.abs(standardized_X.mean(axis=0)).max():.6f}")


# =============================================================================
# 5. PCAで451波長を2つの主成分へ要約する
# =============================================================================

# TODO: PCA(n_components=2)を作り、standardized_Xをpca_scoresへ要約してください
pca = None
pca_scores = None

explained_ratios = pca.explained_variance_ratio_
cumulative_ratio = explained_ratios.sum()

print("PCAの寄与率:", explained_ratios.round(3))
print(f"第1・第2主成分の累積寄与率: {cumulative_ratio:.3f}")


# =============================================================================
# 6. PCAの結果を可視化する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(17, 5))

for lot_id, lot_name in enumerate(lot_names):
    sample_index = np.where(labels == lot_id)[0][0]
    axes[0].plot(wavelengths, X[sample_index], label=lot_name)

axes[0].set_title("Example UV-Vis spectra")
axes[0].set_xlabel("Wavelength (nm)")
axes[0].set_ylabel("Absorbance")
axes[0].legend()
axes[0].grid(alpha=0.25)

for lot_id, lot_name in enumerate(lot_names):
    selected = labels == lot_id
    axes[1].scatter(
        pca_scores[selected, 0],
        pca_scores[selected, 1],
        label=lot_name,
        alpha=0.75,
    )

axes[1].set_title("PCA Score Plot")
axes[1].set_xlabel(f"PC1 ({explained_ratios[0]:.1%})")
axes[1].set_ylabel(f"PC2 ({explained_ratios[1]:.1%})")
axes[1].legend()
axes[1].grid(alpha=0.25)

axes[2].plot(wavelengths, pca.components_[0], label="PC1 loading")
axes[2].plot(wavelengths, pca.components_[1], label="PC2 loading")
axes[2].axhline(0, color="black", linewidth=0.8)
axes[2].set_title("PCA Loadings")
axes[2].set_xlabel("Wavelength (nm)")
axes[2].set_ylabel("Loading")
axes[2].legend()
axes[2].grid(alpha=0.25)

figure.tight_layout()
plt.show()


# =============================================================================
# 結果を読むときの注意
# =============================================================================

print("\n注意：PCAでロットが分かれても、原因物質まで自動的に確定するわけではありません。")
print("原料、濃度、測定日、装置状態などの記録と合わせて原因を確認してください。")
print("ローディングの正負はPCAの計算上反転する場合があり、絶対値と形も確認します。")
