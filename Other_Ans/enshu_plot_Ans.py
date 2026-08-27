# -*- coding: utf-8 -*-
"""
演習：12製造ロットのUV-Visスペクトルを比較する（解答版）

【想定する場面】
飲料工場で12ロットを製造し、品質確認のためUV-Visスペクトルを測定しました。
個別スペクトル、全体平均、ピーク波長の推移をグラフにし、基準から外れた
可能性があるロットを見つけます。

この演習では、折れ線、色、透明度、凡例、基準範囲、複数グラフという
matplotlibの基本を学びます。
"""

# matplotlib：数値データをグラフとして表示します。
import matplotlib.pyplot as plt

# NumPy：波長軸、スペクトル、平均値などを計算します。
import numpy as np


# =============================================================================
# 1. 測定条件と品質基準を設定する
# =============================================================================

# 乱数の種を42に固定し、毎回同じ模擬データを作ります。
rng = np.random.default_rng(42)

# 350 nmから800 nmまでを451点に分けます。ほぼ1 nm間隔です。
wavelengths = np.linspace(350, 800, 451)

# 製品の期待ピーク波長と、許容する上下限を設定します。
expected_peak_nm = 510
lower_limit_nm = 505
upper_limit_nm = 515

# 後でまとめて計算できるよう、スペクトルとピーク波長をリストへ保存します。
spectra = []
detected_peak_wavelengths = []


# =============================================================================
# 2. 12ロットの模擬スペクトルを作る
# =============================================================================

for lot_index in range(12):
    # ロットごとの小さなピーク位置の違いを表します。
    # 最後のロットだけは、変化を見つける練習のため8 nmずらします。
    if lot_index == 11:
        peak_shift = 8.0
    else:
        peak_shift = rng.normal(loc=0.0, scale=2.0)

    # ロットごとの濃度差を想定し、ピークの高さも少し変化させます。
    peak_height = rng.normal(loc=0.85, scale=0.025)

    # ガウス関数で、510 nm付近に釣鐘型の吸収ピークを作ります。
    exponent = -(
        (wavelengths - (expected_peak_nm + peak_shift)) ** 2
    ) / (2 * 35.0 ** 2)
    ideal_absorbance = 0.05 + peak_height * np.exp(exponent)

    # 実測値に似せるため、小さな測定ノイズを加えます。
    noise = rng.normal(loc=0.0, scale=0.012, size=wavelengths.size)
    measured_absorbance = ideal_absorbance + noise

    # append()で、ロットごとの結果をリストへ追加します。
    spectra.append(measured_absorbance)

    # argmax()は最大値がある位置番号を返します。
    # その位置の波長を、観測されたピーク波長として保存します。
    peak_position = np.argmax(measured_absorbance)
    detected_peak_nm = wavelengths[peak_position]
    detected_peak_wavelengths.append(detected_peak_nm)


# =============================================================================
# 3. リストを配列へ変換し、平均スペクトルを求める
# =============================================================================

# spectra_arrayは12行×451列です。1行が1ロットを表します。
spectra_array = np.asarray(spectra)
peak_wavelength_array = np.asarray(detected_peak_wavelengths)

# axis=0は、12ロットの同じ波長同士を縦方向に平均する指定です。
mean_spectrum = spectra_array.mean(axis=0)

# 許容範囲内かどうかをTrue/Falseで判定します。
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

# figureは図全体、axes[0]とaxes[1]は左右のグラフ領域です。
figure, axes = plt.subplots(1, 2, figsize=(15, 5))


# -----------------------------------------------------------------------------
# 左：12ロットのスペクトルと平均スペクトル
# -----------------------------------------------------------------------------

for lot_index, spectrum in enumerate(spectra_array, start=1):
    # 個別ロットは薄い灰色にし、全体傾向を見やすくします。
    axes[0].plot(
        wavelengths,
        spectrum,
        color="gray",
        alpha=0.40,
        linewidth=1.0,
    )

# 平均スペクトルは太い紺色で目立たせます。
axes[0].plot(
    wavelengths,
    mean_spectrum,
    color="navy",
    linewidth=2.5,
    label="Mean spectrum",
)

# 期待ピーク波長を赤い破線で示します。
axes[0].axvline(
    expected_peak_nm,
    color="crimson",
    linestyle="--",
    label="Expected peak",
)

axes[0].set_title("UV-Vis Spectra by Production Lot")
axes[0].set_xlabel("Wavelength (nm)")
axes[0].set_ylabel("Absorbance")
axes[0].legend()
axes[0].grid(alpha=0.25)


# -----------------------------------------------------------------------------
# 右：ロットごとのピーク波長
# -----------------------------------------------------------------------------

lot_numbers = np.arange(1, 13)

# np.where()で、範囲内は青、要確認は赤にします。
point_colors = np.where(within_limits, "steelblue", "crimson")

axes[1].scatter(
    lot_numbers,
    peak_wavelength_array,
    c=point_colors,
    s=80,
    edgecolor="white",
)

# axhspan()は、指定したy範囲を帯状に塗る命令です。
axes[1].axhspan(
    lower_limit_nm,
    upper_limit_nm,
    color="green",
    alpha=0.12,
    label="Acceptable range",
)

axes[1].axhline(expected_peak_nm, color="black", linestyle="--", linewidth=1)
axes[1].set_title("Peak Wavelength by Lot")
axes[1].set_xlabel("Production lot")
axes[1].set_ylabel("Detected peak wavelength (nm)")
axes[1].set_xticks(lot_numbers)
axes[1].legend()
axes[1].grid(alpha=0.25)


# tight_layout()で文字やグラフが重ならないように余白を調整します。
figure.tight_layout()

# 完成した図を表示します。
plt.show()


# =============================================================================
# 結果を使うときの注意
# =============================================================================

print("\n注意：範囲外は自動的な不合格ではなく、再測定や製造記録確認の対象です。")
print("実務の許容範囲は、標準試料、測定精度、過去データを基に決定します。")
