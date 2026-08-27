# -*- coding: utf-8 -*-
"""
演習：分光分析の1日業務を生成・確認・正規化・保存まで通して行う

【想定する場面】
1日の分光測定業務を想定し、8試料分のUV-Visスペクトルを作成し、
CSVとして保存・読み込みし、波長軸を確認したうえで正規化し、
1日分の平均スペクトルを求めてグラフと表に残します。
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


# =============================================================================
# 1. 8試料分の模擬UV-Visスペクトルを作り、CSVへ保存する
# =============================================================================

rng = np.random.default_rng(42)
wavelengths = np.linspace(400, 750, 351)

# 出力先フォルダを作ります（既にあってもエラーにしません）。
output_dir = DATA_DIR / "uv_vis_daily_demo"
output_dir.mkdir(parents=True, exist_ok=True)

for sample_index in range(8):
    peak_height = rng.normal(loc=0.9, scale=0.05)
    peak_center = rng.normal(loc=525, scale=3)

    exponent = -((wavelengths - peak_center) ** 2) / (2 * 34 ** 2)
    absorbance = 0.03 + peak_height * np.exp(exponent)
    absorbance += rng.normal(loc=0.0, scale=0.012, size=wavelengths.size)

    sample_df = pd.DataFrame(
        {
            "wavelength_nm": wavelengths,
            "absorbance": absorbance,
        }
    )
    sample_df.to_csv(output_dir / f"sample_{sample_index + 1:02d}.csv", index=False)


# =============================================================================
# 2. 保存した8個のCSVを読み込む
# =============================================================================

sample_files = sorted(output_dir.glob("sample_*.csv"))
sample_frames = [pd.read_csv(file) for file in sample_files]


# =============================================================================
# 3. 全試料の波長軸が一致しているか確認する
# =============================================================================

# TODO: sample_frames[0]の"wavelength_nm"列をreference_wavelengthsとして取り出し、
#       全試料のwavelength_nm列がreference_wavelengthsと一致するか確認してください
# ヒント： np.allclose(frame["wavelength_nm"], reference_wavelengths)
#         一致しない試料があれば raise ValueError("波長軸が一致しません")
reference_wavelengths = None


# =============================================================================
# 4. 8試料の吸光度を1つの行列にまとめる
# =============================================================================

# TODO: 各frameの"absorbance"列を1行ずつ積み重ねたNumPy配列
#       absorbance_matrix（8行×351列）を作ってください
# ヒント： np.vstack([frame["absorbance"] for frame in sample_frames])
absorbance_matrix = None


# =============================================================================
# 5. 各試料を自分の最大値で正規化し、1日分の平均スペクトルを求める
# =============================================================================

# TODO: absorbance_matrixの各行を、その行の最大値で割った
#       normalized_matrixを作ってください
# ヒント： absorbance_matrix.max(axis=1, keepdims=True) で行ごとの最大値が得られる
normalized_matrix = None

# TODO: normalized_matrixの列ごとの平均を求め、mean_spectrumとしてください
# ヒント： normalized_matrix.mean(axis=0)
mean_spectrum = None


# =============================================================================
# 6. 1日分の平均スペクトルをCSVへ保存する
# =============================================================================

daily_mean_df = pd.DataFrame(
    {
        "wavelength_nm": reference_wavelengths,
        "mean_normalized_absorbance": mean_spectrum,
    }
)
daily_mean_path = output_dir / "daily_mean.csv"
daily_mean_df.to_csv(daily_mean_path, index=False)


# =============================================================================
# 7. 8試料と平均スペクトルをグラフにする
# =============================================================================

for row in normalized_matrix:
    plt.plot(reference_wavelengths, row, alpha=0.45)

plt.plot(
    reference_wavelengths,
    mean_spectrum,
    color="black",
    linewidth=2,
    label="Daily mean",
)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Normalized absorbance")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()

print(f"処理試料数: {len(sample_files)}、保存先: {daily_mean_path}")
