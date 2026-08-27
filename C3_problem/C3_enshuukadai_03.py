# -*- coding: utf-8 -*-
"""
演習：主成分分析（PCA）によるワイン成分の次元削減

（課題概要）
ワインデータセットを用いてPCAを実施し、13個の特徴量を主成分によって
2次元へ要約する。ワインは3種類あり、各主成分の寄与率からデータの
重要な傾向やパターンを把握する。

※ このファイルはTODOを埋める前でも最後まで実行できます（点はすべて原点になります）。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_file_path_uploaded = DATA_DIR / "wine_dataset.csv"

if csv_file_path_uploaded.exists():
    df_wine = pd.read_csv(csv_file_path_uploaded)
else:
    print(f"データが見つからないため、scikit-learn付属のワインデータを使用します: {csv_file_path_uploaded}")
    df_wine = load_wine(as_frame=True).frame

df_wine_x = df_wine.drop('target', axis=1)

scaler = StandardScaler()
df_wine_scaled = scaler.fit_transform(df_wine_x)

pca = PCA(n_components=2)

# TODO: df_wine_scaledをPCAで学習・変換し、principal_componentsを求めてください
# ヒント： pca.fit_transform(df_wine_scaled)
principal_components = np.zeros((len(df_wine_x), 2))

df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
df_pca['target'] = df_wine['target']

plt.figure(figsize=(8, 6))
targets = [0, 1, 2]
colors = ['r', 'g', 'b']
for target, color in zip(targets, colors):
    indices_to_keep = df_pca['target'] == target
    plt.scatter(df_pca.loc[indices_to_keep, 'PC1'],
                df_pca.loc[indices_to_keep, 'PC2'],
                c=color,
                s=50)

plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.title('PCA of Wine Dataset (2 Components)')
plt.legend(targets)
plt.show()
