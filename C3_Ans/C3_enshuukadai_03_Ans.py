from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# -*- coding: utf-8 -*-
# 解答版：背景、前処理、評価指標、結果の限界を確認しながら実行します。
"""
Created on Sun Nov  5 00:29:54 2023

@author: toshiro
"""
# =============================================================================
# ３．主成分分析（PCA）による次元削減: ワインの成分からの分類:
# 
# 課題概要
# 多次元の化学データを解析し、主要なパターンを見つけるためのPCAを実施する。この演習では、scikit-learnのワインデータセット(wine_dataset.csv)を用いてPCAを実施します。目的は、ワインの化学的特性を主成分によって表現し、データの次元を削減することにあります。ワインは３種類です．特徴量１３個より、主成分分析をすることにより，次元削減と，各特徴の寄与率について評価することができます．データの重要な傾向やパターンをより明確に把握することができます。
# 特徴量の詳細
# データセットには以下の特徴量が含まれています：
# 
# アルコール (Alcohol)
# マリック酸 (Malic Acid)
# 灰分 (Ash)
# 灰分のアルカリ度 (Alcalinity of Ash)
# マグネシウム (Magnesium)
# 総フェノール (Total Phenols)
# フラバノイド (Flavanoids)
# 非フラバノイドフェノール (Nonflavanoid Phenols)
# プロアントシアニジン (Proanthocyanins)
# 色の強度 (Color Intensity)
# 色合い (Hue)
# 希釈ワインのOD280/OD315 (OD280/OD315 of Diluted Wines)
# プロリン (Proline)
# =============================================================================


from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt

# ワインデータセットを読み込み
csv_file_path_uploaded = DATA_DIR / "wine_dataset.csv"
df_wine = pd.read_csv(csv_file_path_uploaded)

# PCAのためのデータ準備
df_wine_x = df_wine.drop('target', axis=1)  # PCAのために'target'列を除外

# 特徴量の標準化
scaler = StandardScaler()
df_wine_scaled = scaler.fit_transform(df_wine_x)

# PCAの実行
pca = PCA(n_components=2)  # 可視化のために2つの成分に削減
principal_components = pca.fit_transform(df_wine_scaled)

# PCAの結果のためのDataFrameを作成
df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# PCA DataFrameにターゲット（ワインのタイプ）を追加
df_pca['target'] = df_wine['target']

# PCAの結果をプロット
plt.figure(figsize=(8, 6))
targets = [0, 1, 2]
colors = ['r', 'g', 'b']
for target, color in zip(targets, colors):
    indices_to_keep = df_pca['target'] == target
    plt.scatter(df_pca.loc[indices_to_keep, 'PC1'],
                df_pca.loc[indices_to_keep, 'PC2'],
                c=color,
                s=50)

plt.xlabel('主成分1 (PC1)')
plt.ylabel('主成分2 (PC2)')
plt.title('2成分のPCA')
plt.legend(targets)
plt.show()


