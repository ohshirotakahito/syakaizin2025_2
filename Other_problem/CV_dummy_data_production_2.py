# -*- coding: utf-8 -*-
"""
演習：製造ロット検査用のCV模擬データを作る

CV（サイクリックボルタンメトリー）では、電極へ加える電位を往復させ、
そのとき流れる電流を記録します。物質が酸化・還元される付近では、
電流が山または谷のように変化します。

この演習は、CVの形とPythonの配列処理を学ぶための簡易モデルです。
厳密な電気化学反応を計算する物理モデルではありません。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =============================================================================
# 1. CV測定の条件を設定する
# =============================================================================

start_potential = -0.4
vertex_potential = 0.8
points_each_direction = 400
scan_rate = 0.10


# =============================================================================
# 2. 往復する電位を作る
# =============================================================================

forward_potential = np.linspace(
    start_potential,
    vertex_potential,
    points_each_direction,
)
reverse_potential = np.linspace(
    vertex_potential,
    start_potential,
    points_each_direction,
    endpoint=False,
)
potential = np.concatenate([forward_potential, reverse_potential])
scan_direction = np.array(
    ["Forward"] * len(forward_potential) + ["Reverse"] * len(reverse_potential)
)


# =============================================================================
# 3. 釣鐘型のピークを作る関数を定義する
# =============================================================================

def gaussian_peak(potential_values, center, height, width):
    """中心電位、高さ、幅を指定して、滑らかなピークを作る。"""
    # TODO: ここに実装してください
    # ヒント： exponent = -((potential_values - center) ** 2) / (2 * width ** 2)
    #         return height * np.exp(exponent)
    pass


# =============================================================================
# 4. 往路の酸化電流を作る
# =============================================================================

# 酸化ピークは+0.32 V付近に現れると仮定します（高さ8.0e-6 A、幅0.11）。
oxidation_current = gaussian_peak(
    forward_potential,
    center=0.32,
    height=8.0e-6,
    width=0.11,
)

# ピーク以外にも流れる小さな背景電流を加えます。
forward_current = oxidation_current + 0.8e-6


# =============================================================================
# 5. 復路の還元電流を作る
# =============================================================================

# 還元電流は逆向きに流れるため、負の高さを指定します（中心-0.05 V、高さ-6.5e-6、幅0.13）。
reduction_current = gaussian_peak(
    reverse_potential,
    center=-0.05,
    height=-6.5e-6,
    width=0.13,
)

reverse_current = reduction_current - 0.8e-6

# 往路と復路の電流を1本の配列につなぎます。
ideal_current = np.concatenate([forward_current, reverse_current])


# =============================================================================
# 6. 小さな測定ノイズを加える
# =============================================================================

rng = np.random.default_rng(42)
noise = rng.normal(loc=0.0, scale=0.10e-6, size=potential.size)
measured_current = ideal_current + noise
current_microampere = measured_current * 1.0e6


# =============================================================================
# 7. DataFrameで測定データを整理する
# =============================================================================

cv_data = pd.DataFrame(
    {
        "Potential_V": potential,
        "Current_uA": current_microampere,
        "Direction": scan_direction,
    }
)

print("【CV模擬データ：先頭5行】")
print(cv_data.head())
print(f"\n測定点数: {len(cv_data)}点")
print(f"スキャン速度: {scan_rate:.2f} V/s")


# =============================================================================
# 8. CV曲線を描く
# =============================================================================

figure, axis = plt.subplots(figsize=(9, 6))

axis.plot(
    potential,
    current_microampere,
    color="navy",
    linewidth=1.5,
    label="Simulated measurement",
)

axis.axvline(0.32, color="crimson", linestyle="--", alpha=0.6,
             label="Oxidation peak center")
axis.axvline(-0.05, color="green", linestyle="--", alpha=0.6,
             label="Reduction peak center")
axis.axhline(0, color="black", linewidth=0.8)

axis.set_title("Simulated Cyclic Voltammetry for Production QC")
axis.set_xlabel("Potential (V)")
axis.set_ylabel("Current (µA)")
axis.legend()
axis.grid(alpha=0.25)

figure.tight_layout()
plt.show()


# =============================================================================
# 結果の読み方
# =============================================================================

# ・正方向の山は酸化反応、負方向の谷は還元反応の候補です。
# ・ピーク電位のずれや高さの変化は、試料や電極状態の変化を示すことがあります。
# ・実際の合否判定には、基準試料、繰返し測定、装置校正が必要です。
