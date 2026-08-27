# -*- coding: utf-8 -*-
"""
演習：回転機械の正常・異常振動データを生成する

【想定する場面】
回転機械の正常運転時と、軸ずれ故障時の振動波形を模擬的に作り、
学習データとして保存する。故障時は基本周波数の2倍成分と大きなノイズが
加わる点を波形へ反映する。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)


def generate_vibration_data(num_samples, num_steps, faulty=False):
    """正常または軸ずれ故障を想定した振動波形とラベルを返す。"""
    time = np.linspace(0, 1, num_steps, endpoint=False)
    waves = []

    for _ in range(num_samples):
        # TODO: 回転数の個体差を想定した基本周波数frequencyと位相phaseを決め、
        #       基本の正弦波waveを作ってください
        # ヒント： frequency = rng.normal(12, 0.4)
        #         phase = rng.uniform(0, 2 * np.pi)
        #         wave = np.sin(2 * np.pi * frequency * time + phase)
        frequency = None
        phase = None
        wave = None

        if faulty:
            # TODO: 軸ずれ故障を想定し、2倍周波数成分（振幅0.65）と
            #       大きなノイズ（標準偏差0.28）をwaveへ加えてください
            pass
        else:
            # TODO: 正常時の小さなノイズ（標準偏差0.08）をwaveへ加えてください
            pass
        waves.append(wave)

    label = 1 if faulty else 0
    labels = np.full(num_samples, label, dtype=int)
    return time, np.asarray(waves), labels


num_samples = 120
num_steps = 256
time, normal_data, normal_labels = generate_vibration_data(
    num_samples, num_steps, faulty=False
)
_, faulty_data, faulty_labels = generate_vibration_data(
    num_samples, num_steps, faulty=True
)

# 学習に使えるよう正常・異常を結合します。
all_data = np.vstack([normal_data, faulty_data])
all_labels = np.concatenate([normal_labels, faulty_labels])

# 波形ごとのRMSを計算し、異常時の振動エネルギー増加を確認します。
rms = np.sqrt(np.mean(all_data ** 2, axis=1))
summary = pd.DataFrame({"label": all_labels, "rms": rms})
print("【ラベル別RMS】0=正常、1=軸ずれ故障")
print(summary.groupby("label")["rms"].agg(["count", "mean", "std"]).round(3))

# 波形とラベルを保存します。1行が1つの測定波形です。
output_directory = Path(DATA_DIR)
output_directory.mkdir(exist_ok=True)
columns = [f"time_{i:03d}" for i in range(num_steps)]
output = pd.DataFrame(all_data, columns=columns)
output.insert(0, "fault_label", all_labels)
output.to_csv(output_directory / "motor_vibration_training_data.csv", index=False)

# 正常・異常の代表波形を同じ軸で比較します。
fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=True, sharey=True)
for index in range(3):
    axes[0].plot(time, normal_data[index], alpha=0.8)
    axes[1].plot(time, faulty_data[index], alpha=0.8)
axes[0].set_title("Normal Motor Vibration")
axes[1].set_title("Misalignment Fault Vibration")
axes[1].set_xlabel("Time (seconds)")
for ax in axes:
    ax.set_ylabel("Acceleration (relative unit)")
    ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()
