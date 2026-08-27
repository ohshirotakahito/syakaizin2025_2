# -*- coding: utf-8 -*-
"""
演習：品質検査用クロマトグラムを作成する（解答版）

クロマトグラフィーでは、試料に含まれる成分が時間差で検出器へ到達します。
横軸の「保持時間」は成分が検出されるまでの時間、縦軸の「信号強度」は
検出器の反応の大きさです。山のような形を「ピーク」と呼びます。

この演習では、4成分を含む飲料試料を想定した模擬データを作り、
各ピークの位置、高さ、幅がグラフへどう反映されるかを学びます。
"""

# NumPyは、時間軸の作成や配列全体の計算に使います。
import numpy as np

# pandasは、保持時間と信号強度を表形式で整理するために使います。
import pandas as pd

# matplotlibは、クロマトグラムをグラフとして表示するために使います。
import matplotlib.pyplot as plt


# =============================================================================
# 1. 測定条件を設定する
# =============================================================================

# 0分から15分までを1000個の等間隔な測定点に分けます。
# 点が多いほど、滑らかな曲線として表示できます。
retention_time = np.linspace(0, 15, 1000)

# 装置は成分がなくても完全な0を示すとは限りません。
# ここでは基本となる信号強度を5とします。
baseline_level = 5.0

# 測定時間と同じ長さで、すべてが5の信号配列を作ります。
signal = np.full_like(retention_time, baseline_level)


# =============================================================================
# 2. 試料中の成分とピーク条件を設定する
# =============================================================================

# 各辞書が1つの成分を表します。
# center：ピークの中心となる保持時間（分）
# height：ベースラインから見たピークの高さ
# width ：ピークの広がり。大きいほど横に広いピークになります。
components = [
    {"name": "Vitamin C", "center": 3.0, "height": 10.0, "width": 0.10},
    {"name": "Caffeine", "center": 5.0, "height": 15.0, "width": 0.30},
    {"name": "Preservative A", "center": 8.0, "height": 7.0, "width": 0.30},
    {"name": "Preservative B", "center": 9.5, "height": 9.0, "width": 0.50},
]


# =============================================================================
# 3. ガウス関数を使ってピークを作る
# =============================================================================

# 関数にすると、同じ計算を成分ごとに繰り返し利用できます。
def gaussian_peak(time_values, center, height, width):
    """指定した中心、高さ、幅を持つ釣鐘型のピークを返す。"""

    # time_values - centerで、各時点が中心からどれだけ離れているか求めます。
    # np.exp()を含むこの式により、中心が最も高い滑らかな釣鐘型になります。
    exponent = -((time_values - center) ** 2) / (2 * width ** 2)
    return height * np.exp(exponent)


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

# 乱数の種を42に固定すると、実行するたびに同じ結果を再現できます。
rng = np.random.default_rng(42)

# 平均0、標準偏差0.12の小さな正規分布ノイズを1000個作ります。
noise = rng.normal(loc=0.0, scale=0.12, size=retention_time.size)

# 理想的な信号へノイズを加え、模擬測定信号を作ります。
measured_signal = signal + noise


# =============================================================================
# 5. DataFrameで測定データを表にする
# =============================================================================

# DataFrameは、列名を持つ表形式のデータです。
chromatogram = pd.DataFrame(
    {
        "Retention_Time_min": retention_time,
        "Signal_Intensity": measured_signal,
    }
)

# head()で表の先頭5行を確認します。
print("【クロマトグラムデータ：先頭5行】")
print(chromatogram.head())

# 成分名と設定した保持時間も一覧表示します。
print("\n【想定した成分と保持時間】")
for component in components:
    print(f"{component['name']}: {component['center']:.1f}分")


# =============================================================================
# 6. クロマトグラムをグラフにする
# =============================================================================

# figsizeは、グラフ全体の横幅と縦幅をインチ単位で指定します。
figure, axis = plt.subplots(figsize=(11, 6))

# retention_timeを横軸、measured_signalを縦軸として線を描きます。
axis.plot(
    retention_time,
    measured_signal,
    color="navy",
    linewidth=1.2,
    label="Measured signal",
)

# 各成分の保持時間に赤い破線と成分名を追加します。
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

# タイトル、軸名、凡例、補助線を加えると、グラフを読みやすくできます。
axis.set_title("Simulated Beverage Quality-control Chromatogram")
axis.set_xlabel("Retention time (min)")
axis.set_ylabel("Signal intensity")
axis.legend()
axis.grid(alpha=0.25)

# 文字が描画領域からはみ出しにくいように余白を自動調整します。
figure.tight_layout()

# 完成したクロマトグラムを表示します。
plt.show()


# =============================================================================
# 結果の読み方
# =============================================================================

# ・ピーク中心の時間は、成分を識別する手掛かりになります。
# ・ピークの高さや面積は、成分量を推定する手掛かりになります。
# ・ただし実際の定量には、標準試料による検量線や装置条件の確認が必要です。
