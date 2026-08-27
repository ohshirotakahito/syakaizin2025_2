# -*- coding: utf-8 -*-
"""
演習：製造ロット検査用のCV模擬データを作る（解答版）

CV（サイクリックボルタンメトリー）では、電極へ加える電位を往復させ、
そのとき流れる電流を記録します。物質が酸化・還元される付近では、
電流が山または谷のように変化します。

この演習は、CVの形とPythonの配列処理を学ぶための簡易モデルです。
厳密な電気化学反応を計算する物理モデルではありません。
"""

# NumPy：電位・電流の配列計算と乱数生成に使います。
import numpy as np

# pandas：計算した測定値を列名付きの表へ整理します。
import pandas as pd

# matplotlib：CV曲線をグラフとして表示します。
import matplotlib.pyplot as plt


# =============================================================================
# 1. CV測定の条件を設定する
# =============================================================================

# 最初に電極へ加える電位です。単位はV（ボルト）です。
start_potential = -0.4

# 折り返し地点の電位です。ここへ到達した後、開始電位へ戻ります。
vertex_potential = 0.8

# 往路と復路にそれぞれ400個の測定点を作ります。
points_each_direction = 400

# スキャン速度は、1秒間に変化させる電位です。
# 今回は表示用の測定条件として使います。
scan_rate = 0.10


# =============================================================================
# 2. 往復する電位を作る
# =============================================================================

# np.linspace()で開始電位から頂点電位までの往路を作ります。
forward_potential = np.linspace(
    start_potential,
    vertex_potential,
    points_each_direction,
)

# endpoint=Falseにすると、頂点電位が往路と復路で重複するのを防げます。
reverse_potential = np.linspace(
    vertex_potential,
    start_potential,
    points_each_direction,
    endpoint=False,
)

# concatenate()は複数の配列を前後につなぐ関数です。
potential = np.concatenate([forward_potential, reverse_potential])

# 往路と復路を区別する文字列の配列も作ります。
scan_direction = np.array(
    ["Forward"] * len(forward_potential) + ["Reverse"] * len(reverse_potential)
)


# =============================================================================
# 3. 釣鐘型のピークを作る関数を定義する
# =============================================================================

def gaussian_peak(potential_values, center, height, width):
    """中心電位、高さ、幅を指定して、滑らかなピークを作る。"""

    exponent = -((potential_values - center) ** 2) / (2 * width ** 2)
    return height * np.exp(exponent)


# =============================================================================
# 4. 往路の酸化電流を作る
# =============================================================================

# 酸化ピークは+0.32 V付近に現れると仮定します。
# 電流はA（アンペア）で表し、8e-6 Aは8 µAです。
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

# 還元電流は逆向きに流れるため、負の高さを指定します。
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

# 42を固定すると、毎回同じノイズを再現できます。
rng = np.random.default_rng(42)

# 平均0 A、標準偏差0.10 µAの小さなノイズを作ります。
noise = rng.normal(loc=0.0, scale=0.10e-6, size=potential.size)

# 理想電流とノイズを足して、模擬測定電流を作ります。
measured_current = ideal_current + noise

# Aでは値が小さいので、見やすいµAへ変換します。1 A = 1,000,000 µAです。
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

# 横軸を電位、縦軸を電流として、往路と復路がつながった曲線を描きます。
axis.plot(
    potential,
    current_microampere,
    color="navy",
    linewidth=1.5,
    label="Simulated measurement",
)

# 酸化・還元ピークの中心電位を破線で示します。
axis.axvline(0.32, color="crimson", linestyle="--", alpha=0.6,
             label="Oxidation peak center")
axis.axvline(-0.05, color="green", linestyle="--", alpha=0.6,
             label="Reduction peak center")

# 電流0 µAの位置を横線で示すと、正負を読み取りやすくなります。
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
