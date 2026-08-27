# -*- coding: utf-8 -*-
"""
演習：教師なし学習によるクラスタリングでワインを分類する

（課題概要）
ワインのサンプルデータを用いて教師なし分類を行う。13種類の特徴量を用いて、
KMeansアルゴリズムでサンプルをクラスタに分類する。target列（ワインの種類）
はクラスタリング自体には使用しない。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

csv_file_path_uploaded = DATA_DIR / "wine_dataset.csv"

if csv_file_path_uploaded.exists():
    df_uploaded = pd.read_csv(csv_file_path_uploaded)
else:
    print(f"データが見つからないため、scikit-learn付属のワインデータを使用します: {csv_file_path_uploaded}")
    wine_bunch = load_wine(as_frame=True)
    df_uploaded = wine_bunch.frame

X = df_uploaded.drop('target', axis=1)

# TODO: n_clusters=3のKMeansを作成し、Xでfit()してください
# ヒント： KMeans(n_clusters=3, random_state=42).fit(X)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.labels_ = np.zeros(len(X), dtype=int)  # 仮実装（未学習）

df_uploaded['cluster'] = kmeans.labels_

pairplot_columns = ['alcohol', 'malic_acid', 'total_phenols', 'color_intensity', 'cluster']
sns.pairplot(df_uploaded[pairplot_columns], hue='cluster', palette='Set2')

plt.show()
