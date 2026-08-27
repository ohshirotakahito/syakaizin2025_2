# -*- coding: utf-8 -*-
"""
演習：品質検査用クロマトグラムを作成する

クロマトグラフィーでは、試料に含まれる成分が時間差で検出器へ到達します。
横軸の「保持時間」は成分が検出されるまでの時間、縦軸の「信号強度」は
検出器の反応の大きさです。山のような形を「ピーク」と呼びます。

この演習では、4成分を含む飲料試料を想定した模擬データを作り、
各ピークの位置、高さ、幅がグラフへどう反映されるかを学びます。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =============================================================================
# 1. 測定条件を設定する
# =============================================================================

retention_time = np.linspace(0, 15, 1000)
baseline_level = 5.0
signal = np.full_like(retention_time, baseline_level)


# =============================================================================
# 2. 試料中の成分とピーク条件を設定する
# =============================================================================

components = [
    {"name": "Vitamin C", "center": 3.0, "height": 10.0, "width": 0.10},
    {"name": "Caffeine", "center": 5.0, "height": 15.0, "width": 0.30},
    {"name": "Preservative A", "center": 8.0, "height": 7.0, "width": 0.30},
    {"name": "Preservative B", "center": 9.5, "height": 9.0, "width": 0.50},
]


# =============================================================================
# 3. ガウス関数を使ってピークを作る
# =============================================================================

def gaussian_peak(time_values, center, height, width):
    """指定した中心、高さ、幅を持つ釣鐘型のピークを返す。"""
    # TODO: ここに実装してください
    # ヒント： exponent = -((time_values - center) ** 2) / (2 * width ** 2)
    #         return height * np.exp(exponent)
    pass


# 各成分のピークを作り、現在のsignalへ順番に加えます。
for component in components:
    peak = gaussian_peak(
        retention_time,
        component["center"],
        component["height"],
        component["width"],
    )
    signal = signal + peak


# =============================================================================
# 4. 実際の測定に近づけるため、小さなノイズを加える
# =============================================================================

rng = np.random.default_rng(42)
noise = rng.normal(loc=0.0, scale=0.12, size=retention_time.size)
measured_signal = signal + noise


# =============================================================================
# 5. DataFrameで測定データを表にする
# =============================================================================

chromatogram = pd.DataFrame(
    {
        "Retention_Time_min": retention_time,
        "Signal_Intensity": measured_signal,
    }
)

print("【クロマトグラムデータ：先頭5行】")
print(chromatogram.head())

print("\n【想定した成分と保持時間】")
for component in components:
    print(f"{component['name']}: {component['center']:.1f}分")


# =============================================================================
# 6. クロマトグラムをグラフにする
# =============================================================================

figure, axis = plt.subplots(figsize=(11, 6))

axis.plot(
    retention_time,
    measured_signal,
    color="navy",
    linewidth=1.2,
    label="Measured signal",
)

for component in components:
    center = component["center"]
    axis.axvline(center, color="crimson", linestyle="--", alpha=0.45)
    axis.text(
        center,
        baseline_level + component["height"] + 0.8,
        component["name"],
        rotation=90,
        ha="center",
        va="bottom",
        fontsize=9,
    )

axis.set_title("Simulated Beverage Quality-control Chromatogram")
axis.set_xlabel("Retention time (min)")
axis.set_ylabel("Signal intensity")
axis.legend()
axis.grid(alpha=0.25)

figure.tight_layout()
plt.show()


# =============================================================================
# 結果の読み方
# =============================================================================

# ・ピーク中心の時間は、成分を識別する手掛かりになります。
# ・ピークの高さや面積は、成分量を推定する手掛かりになります。
# ・ただし実際の定量には、標準試料による検量線や装置条件の確認が必要です。
