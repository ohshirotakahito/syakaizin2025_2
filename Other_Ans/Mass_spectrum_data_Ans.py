# -*- coding: utf-8 -*-
"""解答版：食品包装材の溶出試験を想定した質量スペクトル解析。"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

rng = np.random.default_rng(42)
mz = np.linspace(50, 500, 4501)

# 既知物質ライブラリと、未知試料に含まれるピークを設定します。
library = pd.DataFrame({
    "compound": ["Solvent residue", "Antioxidant fragment", "Plasticizer fragment",
                 "Internal standard"],
    "reference_mz": [91.1, 149.0, 279.2, 350.2],
})
sample_peaks = [(91.1, 480, 0.35), (149.0, 820, 0.45),
                (224.3, 260, 0.55), (279.2, 610, 0.60), (350.2, 1200, 0.40)]

intensity = np.full_like(mz, 25.0)
for center, height, width in sample_peaks:
    intensity += height * np.exp(-((mz - center) ** 2) / (2 * width ** 2))
intensity = np.clip(intensity + rng.normal(0, 12, mz.size), 0, None)

# 高さ150以上、十分な間隔のあるピークを自動検出します。
peak_indexes, properties = find_peaks(intensity, height=150, distance=10, prominence=80)
detected = pd.DataFrame({
    "detected_mz": mz[peak_indexes],
    "intensity": intensity[peak_indexes],
})

# ライブラリm/zとの差が0.5以内なら既知物質候補として割り当てます。
def identify_compound(detected_mz):
    differences = (library["reference_mz"] - detected_mz).abs()
    nearest_index = differences.idxmin()
    if differences.loc[nearest_index] <= 0.5:
        return library.loc[nearest_index, "compound"]
    return "Unknown - confirmation required"


detected["candidate"] = detected["detected_mz"].apply(identify_compound)
detected["relative_intensity_percent"] = (
    detected["intensity"] / intensity.max() * 100
)

print("【検出ピークと同定候補】")
print(detected.round(2).to_string(index=False))
print("\n注意：m/z一致は候補提示であり、物質同定の確定ではありません。")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(mz, intensity / intensity.max() * 100, color="#345995", linewidth=1)
ax.scatter(detected["detected_mz"], detected["relative_intensity_percent"],
           color="#E45756", zorder=3, label="Detected peaks")
for row in detected.itertuples():
    ax.annotate(f"{row.detected_mz:.1f}\n{row.candidate}",
                (row.detected_mz, row.relative_intensity_percent),
                xytext=(5, 8), textcoords="offset points", fontsize=7, rotation=35)
ax.set_xlabel("Mass-to-charge ratio (m/z)")
ax.set_ylabel("Relative intensity (%)")
ax.set_title("Extractables Screening of Food Packaging")
ax.grid(alpha=0.2)
ax.legend()
fig.tight_layout()
plt.show()

