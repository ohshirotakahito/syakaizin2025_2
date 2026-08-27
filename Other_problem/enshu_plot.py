# -*- coding: utf-8 -*-
"""
演習：12製造ロットのUV-Visスペクトルを比較する

【想定する場面】
飲料工場で12ロットを製造し、品質確認のためUV-Visスペクトルを測定しました。
個別スペクトル、全体平均、ピーク波長の推移をグラフにし、基準から外れた
可能性があるロットを見つけます。

この演習では、折れ線、色、透明度、凡例、基準範囲、複数グラフという
matplotlibの基本を学びます。
"""

import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# 1. 測定条件と品質基準を設定する
# =============================================================================

rng = np.random.default_rng(42)
wavelengths = np.linspace(350, 800, 451)

expected_peak_nm = 510
lower_limit_nm = 505
upper_limit_nm = 515

spectra = []
detected_peak_wavelengths = []


# =============================================================================
# 2. 12ロットの模擬スペクトルを作る
# =============================================================================

for lot_index in range(12):
    if lot_index == 11:
        peak_shift = 8.0
    else:
        peak_shift = rng.normal(loc=0.0, scale=2.0)

    peak_height = rng.normal(loc=0.85, scale=0.025)

    exponent = -(
        (wavelengths - (expected_peak_nm + peak_shift)) ** 2
    ) / (2 * 35.0 ** 2)
    ideal_absorbance = 0.05 + peak_height * np.exp(exponent)

    noise = rng.normal(loc=0.0, scale=0.012, size=wavelengths.size)
    measured_absorbance = ideal_absorbance + noise

    spectra.append(measured_absorbance)

    peak_position = np.argmax(measured_absorbance)
    detected_peak_nm = wavelengths[peak_position]
    detected_peak_wavelengths.append(detected_peak_nm)


# =============================================================================
# 3. リストを配列へ変換し、平均スペクトルを求める
# =============================================================================

spectra_array = np.asarray(spectra)
peak_wavelength_array = np.asarray(detected_peak_wavelengths)

mean_spectrum = spectra_array.mean(axis=0)

within_limits = (
    (peak_wavelength_array >= lower_limit_nm)
    & (peak_wavelength_array <= upper_limit_nm)
)


# =============================================================================
# 4. ピーク波長と判定結果を表示する
# =============================================================================

print("【ロット別ピーク波長】")
for lot_index, (peak_nm, is_within) in enumerate(
    zip(peak_wavelength_array, within_limits),
    start=1,
):
    status = "範囲内" if is_within else "要確認"
    print(f"Lot {lot_index:02d}: {peak_nm:.1f} nm  {status}")

print(f"\n要確認ロット数: {np.count_nonzero(~within_limits)}件")


# =============================================================================
# 5. グラフを横に2つ並べる
# =============================================================================

figure, axes = plt.subplots(1, 2, figsize=(15, 5))


# -----------------------------------------------------------------------------
# 左：12ロットのスペクトルと平均スペクトル
# -----------------------------------------------------------------------------

# TODO: spectra_arrayの各ロットを薄い灰色（color="gray", alpha=0.40）で
#       axes[0]に描いてください
# TODO: mean_spectrumを太い紺色（color="navy", linewidth=2.5,
#       label="Mean spectrum"）でaxes[0]に描いてください
# TODO: 期待ピーク波長expected_peak_nmを赤い破線（axes[0].axvline）で示してください

axes[0].set_title("UV-Vis Spectra by Production Lot")
axes[0].set_xlabel("Wavelength (nm)")
axes[0].set_ylabel("Absorbance")
axes[0].legend()
axes[0].grid(alpha=0.25)


# -----------------------------------------------------------------------------
# 右：ロットごとのピーク波長
# -----------------------------------------------------------------------------

lot_numbers = np.arange(1, 13)

# TODO: within_limitsを使って、範囲内は"steelblue"、要確認は"crimson"になる
#       色の配列point_colorsを作ってください（np.whereを使うと簡単）
point_colors = None

# TODO: axes[1].scatter()で、lot_numbersを横軸、peak_wavelength_arrayを縦軸に、
#       point_colorsで色分けした散布図を描いてください

# TODO: axes[1].axhspan()で、lower_limit_nmからupper_limit_nmまでを
#       緑色の帯（color="green", alpha=0.12, label="Acceptable range"）で示してください

axes[1].axhline(expected_peak_nm, color="black", linestyle="--", linewidth=1)
axes[1].set_title("Peak Wavelength by Lot")
axes[1].set_xlabel("Production lot")
axes[1].set_ylabel("Detected peak wavelength (nm)")
axes[1].set_xticks(lot_numbers)
axes[1].legend()
axes[1].grid(alpha=0.25)


figure.tight_layout()
plt.show()


# =============================================================================
# 結果を使うときの注意
# =============================================================================

print("\n注意：範囲外は自動的な不合格ではなく、再測定や製造記録確認の対象です。")
print("実務の許容範囲は、標準試料、測定精度、過去データを基に決定します。")
