# -*- coding: utf-8 -*-
"""解答版：分光分析の1日業務を生成・確認・正規化・保存まで通して行う。"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng=np.random.default_rng(42); axis=np.linspace(400,750,351)
data_dir=Path(DATA_DIR / "uv_vis_daily_demo"); data_dir.mkdir(parents=True,exist_ok=True)
for sample in range(8):
    absorbance=.03+rng.normal(.9,.05)*np.exp(-((axis-rng.normal(525,3))**2)/(2*34**2))
    absorbance+=rng.normal(0,.012,axis.size)
    pd.DataFrame({"wavelength_nm":axis,"absorbance":absorbance}).to_csv(data_dir/f"sample_{sample+1:02d}.csv",index=False)
files=sorted(data_dir.glob("sample_*.csv")); frames=[pd.read_csv(file) for file in files]
reference=frames[0]["wavelength_nm"].to_numpy()
if any(not np.allclose(frame["wavelength_nm"],reference) for frame in frames): raise ValueError("波長軸が一致しません")
matrix=np.vstack([frame["absorbance"] for frame in frames])
normalized=matrix/matrix.max(axis=1,keepdims=True); mean_spectrum=normalized.mean(axis=0)
pd.DataFrame({"wavelength_nm":reference,"mean_normalized_absorbance":mean_spectrum}).to_csv(data_dir/"daily_mean.csv",index=False)
for row in normalized: plt.plot(reference,row,alpha=.45)
plt.plot(reference,mean_spectrum,color="black",linewidth=2,label="Daily mean")
plt.xlabel("Wavelength (nm)"); plt.ylabel("Normalized absorbance"); plt.legend(); plt.grid(alpha=.2)
plt.tight_layout(); plt.show(); print(f"処理試料数: {len(files)}、保存先: {data_dir/'daily_mean.csv'}")
