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
# ２．教師なし学習によるクラスタリング：ワインの分類をする
# 
# （課題概要）
# この課題では、ワインのサンプルデータ（wine_dataset.csv）を用いて教師なし分類を行います。データセットには、異なるワインサンプルの13種類の特徴量が含まれています。これらの特徴量を用いて、KMeansアルゴリズムを使用し、サンプルをクラスタに分類してください。ただし、Target列はワインの種類を示しているため、この課題では使用しません。
# 
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


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# CSVファイルの内容を読み込んで表示
csv_file_path_uploaded = DATA_DIR / "wine_dataset.csv"
df_uploaded = pd.read_csv(csv_file_path_uploaded)

# クラスタリングのためのデータ準備
X = df_uploaded.drop('target', axis=1)  # クラスタリングのために'target'列を除外

# KMeansクラスタリングを実行
# ワインデータセットには通常3種類のワインがあるため、初期的に3つのクラスタを想定
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# データセットにクラスタラベルを追加
df_uploaded['cluster'] = kmeans.labels_

# 特徴量のサブセットを使用してクラスタをペアプロットで視覚化
pairplot_columns = ['alcohol', 'malic_acid', 'total_phenols', 'color_intensity', 'cluster']
sns.pairplot(df_uploaded[pairplot_columns], hue='cluster', palette='Set2')

plt.show()


