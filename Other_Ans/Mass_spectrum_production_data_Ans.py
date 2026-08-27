# -*- coding: utf-8 -*-
"""解答版：製造ライン洗浄後の残留物を模した質量スペクトルを生成する。"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 同じ演習結果を再現できるよう乱数を固定します。
rng = np.random.default_rng(42)

# m/z 50〜500を0.1刻み相当で測定した状況を作ります。
mz = np.linspace(50, 500, 4501)

# 既知の洗浄剤断片・製品残留物・内部標準を想定したピーク情報です。
peak_table = pd.DataFrame({
    "compound": ["Cleaning agent A", "Product fragment 1", "Product fragment 2",
                 "Internal standard", "Packaging additive", "Unknown trace"],
    "center_mz": [108.1, 168.2, 238.3, 289.2, 371.4, 454.1],
    "height": [420, 1250, 760, 1800, 310, 190],
    "width": [0.35, 0.55, 0.70, 0.40, 0.85, 0.60],
})

# 装置由来の緩やかなベースラインを作ります。
baseline = 35 + 0.025 * (mz - 50)
intensity = baseline.copy()

# 各化合物のピークをガウス関数で加算します。
for row in peak_table.itertuples():
    peak = row.height * np.exp(-((mz - row.center_mz) ** 2) / (2 * row.width ** 2))
    intensity += peak

# 電気的・化学的な測定ノイズを加え、負の強度は0へ補正します。
intensity += rng.normal(0, 18, mz.size)
intensity = np.clip(intensity, 0, None)

# 解析用の表へ変換します。
spectrum = pd.DataFrame({"mz": mz, "intensity": intensity})

# 最大強度を100とする相対強度も追加します。
spectrum["relative_intensity_percent"] = (
    spectrum["intensity"] / spectrum["intensity"].max() * 100
)

print("【設定したピーク】")
print(peak_table.to_string(index=False))
print(f"\nデータ点数: {len(spectrum):,}")
print(f"最大強度: {spectrum['intensity'].max():.1f}")

# dataフォルダを必要に応じて作り、CSVへ保存します。
output_directory = Path(DATA_DIR)
output_directory.mkdir(exist_ok=True)
output_path = output_directory / "qc_mass_spectrum.csv"
spectrum.to_csv(output_path, index=False)
print(f"保存先: {output_path}")

# スペクトルと既知ピーク位置を表示します。
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(spectrum["mz"], spectrum["relative_intensity_percent"],
        color="#345995", linewidth=1)
for row in peak_table.itertuples():
    ax.axvline(row.center_mz, color="#E45756", alpha=0.25, linestyle="--")
    ax.text(row.center_mz, 103, row.compound, rotation=90,
            va="bottom", ha="center", fontsize=7)
ax.set_xlabel("Mass-to-charge ratio (m/z)")
ax.set_ylabel("Relative intensity (%)")
ax.set_title("QC Mass Spectrum after Production-line Cleaning")
ax.set_ylim(0, 122)
ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()

