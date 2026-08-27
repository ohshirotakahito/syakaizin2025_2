# -*- coding: utf-8 -*-
"""
演習：UV-VisスペクトルをPCAで要約し、製造ロットを比較する（解答版）

【想定する場面】
飲料工場で同じ製品を3つの製造ロットに分けて生産しました。UV-Vis測定では、
1試料につき451波長の吸光度が得られます。451個の数値をそのまま比較する
代わりに、PCA（主成分分析）で2個の主成分へ要約します。

PCAは正解ラベルを使わず、データのばらつきが大きい方向を見つける
「教師なし学習」です。スコアとローディングは役割が異なります。
"""

# matplotlib：スペクトル、PCAスコア、ローディングを表示します。
import matplotlib.pyplot as plt

# NumPy：波長軸、スペクトル、配列を扱います。
import numpy as np

# PCA：多数の波長を少数の主成分へ要約します。
from sklearn.decomposition import PCA

# StandardScaler：波長ごとの平均を0、標準偏差を1へ近づけます。
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 模擬UV-Visスペクトルを作る条件
# =============================================================================

# 乱数の種を固定し、実行するたびに同じ模擬データを作ります。
rng = np.random.default_rng(42)

# 350 nmから800 nmまでを451点に分けます。ほぼ1 nm間隔です。
wavelengths = np.linspace(350, 800, 451)

# 3ロットの名前と、代表的な吸収ピーク位置です。
lot_names = ["Lot A", "Lot B", "Lot C"]
peak_centers = [470, 520, 575]

# 作成したスペクトルとロット番号を保存する空リストです。
spectra = []
lot_labels = []


# =============================================================================
# 2. 3ロット×18試料の模擬スペクトルを作る
# =============================================================================

for lot_id, peak_center in enumerate(peak_centers):
    for _ in range(18):
        # 試料差を表すため、ピーク中心を標準偏差3 nmで少しずらします。
        shifted_center = rng.normal(loc=peak_center, scale=3.0)

        # ガウス関数で釣鐘型の吸収ピークを作ります。
        exponent = -((wavelengths - shifted_center) ** 2) / (2 * 32.0 ** 2)
        absorption_peak = np.exp(exponent)

        # ベースライン吸光度0.04と、小さな測定ノイズを加えます。
        noise = rng.normal(loc=0.0, scale=0.015, size=wavelengths.size)
        measured_spectrum = 0.04 + absorption_peak + noise

        spectra.append(measured_spectrum)
        lot_labels.append(lot_id)


# =============================================================================
# 3. NumPy配列へ変換し、データの形を確認する
# =============================================================================

# 1行が1試料、1列が1波長になる54行×451列の配列です。
X = np.asarray(spectra)
labels = np.asarray(lot_labels)

print("【UV-Vis模擬データ】")
print(f"Xの形: {X.shape}（試料数, 波長数）")
print(f"ロット数: {len(lot_names)}")


# =============================================================================
# 4. 波長ごとに標準化する
# =============================================================================

# fit_transform()は次の2処理をまとめて行います。
# fit：各波長の平均と標準偏差を計算
# transform：計算結果を使って標準化
scaler = StandardScaler()
standardized_X = scaler.fit_transform(X)

# 標準化すると各波長を同じ尺度で比較できます。ただし、信号変化がほとんど
# ない波長の小さなノイズも強調される可能性がある点に注意が必要です。
print("標準化後の全列平均の絶対最大値: "
      f"{np.abs(standardized_X.mean(axis=0)).max():.6f}")


# =============================================================================
# 5. PCAで451波長を2つの主成分へ要約する
# =============================================================================

# n_components=2は、第1主成分と第2主成分を求める指定です。
pca = PCA(n_components=2)

# pca_scoresは各試料の新しい座標です。形は54行×2列になります。
pca_scores = pca.fit_transform(standardized_X)

# 寄与率は、各主成分が元データのばらつきをどれだけ説明するかを表します。
explained_ratios = pca.explained_variance_ratio_
cumulative_ratio = explained_ratios.sum()

print("PCAの寄与率:", explained_ratios.round(3))
print(f"第1・第2主成分の累積寄与率: {cumulative_ratio:.3f}")


# =============================================================================
# 6. PCAの結果を可視化する
# =============================================================================

figure, axes = plt.subplots(1, 3, figsize=(17, 5))

# 左：各ロットから1試料ずつ、元のUV-Visスペクトルを表示します。
for lot_id, lot_name in enumerate(lot_names):
    sample_index = np.where(labels == lot_id)[0][0]
    axes[0].plot(wavelengths, X[sample_index], label=lot_name)

axes[0].set_title("Example UV-Vis spectra")
axes[0].set_xlabel("Wavelength (nm)")
axes[0].set_ylabel("Absorbance")
axes[0].legend()
axes[0].grid(alpha=0.25)

# 中央：スコアプロットです。1点が1試料を表します。
# 同じロットの点が近ければ、スペクトル全体の特徴が似ています。
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

# 右：ローディングです。各波長が主成分へ与える重みを表します。
# 絶対値が大きい波長ほど、その主成分による違いへ強く関係します。
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
