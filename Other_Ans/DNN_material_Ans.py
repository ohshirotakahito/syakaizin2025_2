# -*- coding: utf-8 -*-
"""
演習：材料特性から耐久年数をニューラルネットワークで予測する（解答版）

【想定する場面】
材料メーカーで、新しい材料候補の耐久試験には長い時間が必要です。そこで、
過去に試験した材料の物性値と配合比率から、耐久年数の目安を予測します。

ここではscikit-learnのMLPRegressorを使います。MLPは複数の層で数値の関係を
学習するニューラルネットワークです。「DNN」という言葉は一般に層の深い
ニューラルネットワークを指しますが、この演習では学習しやすい小規模な
多層パーセプトロンを使用します。
"""

# Path：実行場所に依存しないデータファイルの場所を作ります。
from pathlib import Path

# matplotlib：正解値と予測値をグラフで比較します。
import matplotlib.pyplot as plt

# NumPy：ベースライン予測用の数値配列を作ります。
import numpy as np

# pandas：CSVを表形式のDataFrameとして扱います。
import pandas as pd

# 評価指標：MAE、MSE、R²を計算します。
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# データを学習用とテスト用に分けます。
from sklearn.model_selection import train_test_split

# MLPRegressor：数値を予測するニューラルネットワークです。
from sklearn.neural_network import MLPRegressor

# Pipeline：標準化とモデルを順番に実行する仕組みです。
from sklearn.pipeline import make_pipeline

# StandardScaler：列ごとの平均を0、標準偏差を1に近づけます。
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 材料データを読み込む
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# まずdataset3を使用し、なければdataset1を使用します。
data_path = DATA_DIR / "material_science_dataset3.csv"
if not data_path.exists():
    data_path = DATA_DIR / "material_science_dataset1.csv"

if not data_path.exists():
    raise FileNotFoundError("材料データがdataフォルダに見つかりません。")

materials = pd.read_csv(data_path)

print("【使用するデータ】")
print(f"ファイル: {data_path.name}")
print(f"行数: {len(materials)}、列数: {len(materials.columns)}")
print(materials.head())


# =============================================================================
# 2. 特徴量Xと正解yを分ける
# =============================================================================

# この列が予測したい正解値（目的変数）です。
target_column = "Existing_Durability_Years"

# drop()で正解列を除き、残りの物性値と配合比率を特徴量にします。
features = materials.drop(columns=[target_column])

# 正解列だけを取り出します。
target = materials[target_column]

print("\n【特徴量】")
for column_name in features.columns:
    print(f"・{column_name}")


# =============================================================================
# 3. 学習用データとテスト用データに分ける
# =============================================================================

# test_size=0.2は、全体の20%をテスト専用にする指定です。
# random_state=42により、毎回同じ分け方を再現できます。
X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.2,
    random_state=42,
)

print(f"\n学習データ: {len(X_train)}件")
print(f"テストデータ: {len(X_test)}件")


# =============================================================================
# 4. 標準化とニューラルネットワークを組み合わせる
# =============================================================================

# 材料データはMPa、℃、GPa、%など、列によって単位と桁が異なります。
# StandardScalerで尺度を揃えると、一部の列だけが強く影響するのを防げます。
#
# hidden_layer_sizes=(32, 16)：中間層を32個、16個のニューロンで構成
# solver="lbfgs"              ：小規模データで使いやすい学習方法
# max_iter=3000               ：学習を繰り返す上限
# random_state=42             ：初期値を固定して結果を再現
model = make_pipeline(
    StandardScaler(),
    MLPRegressor(
        hidden_layer_sizes=(32, 16),
        solver="lbfgs",
        max_iter=3000,
        random_state=42,
    ),
)


# =============================================================================
# 5. モデルを学習し、未知データを予測する
# =============================================================================

# fit()は、学習用の特徴量と正解値の関係をモデルへ学習させます。
model.fit(X_train, y_train)

# predict()は、学習に使用していないテストデータの耐久年数を予測します。
predicted_years = model.predict(X_test)


# =============================================================================
# 6. 予測性能を数値で評価する
# =============================================================================

# MAE：予測誤差の絶対値の平均です。単位は年なので直感的に読めます。
mae = mean_absolute_error(y_test, predicted_years)

# MSE：大きな誤差をより強く評価します。小さいほど良い値です。
mse = mean_squared_error(y_test, predicted_years)

# R²：1に近いほど正解の変動をよく説明します。
# 0以下の場合は、単純に平均値を予測する方法より悪い可能性があります。
r2 = r2_score(y_test, predicted_years)

# 比較のため、すべてを学習データの平均値と予測する単純モデルを作ります。
baseline_prediction = np.full(len(y_test), y_train.mean())
baseline_mae = mean_absolute_error(y_test, baseline_prediction)

print("\n【モデルの評価】")
print(f"ニューラルネットワークのMAE: {mae:.3f}年")
print(f"平均値だけで予測した場合のMAE: {baseline_mae:.3f}年")
print(f"MSE: {mse:.3f}")
print(f"R²: {r2:.3f}")


# =============================================================================
# 7. 正解値と予測値を表で比較する
# =============================================================================

comparison = pd.DataFrame(
    {
        "Actual_Years": y_test.to_numpy(),
        "Predicted_Years": predicted_years,
    }
)
comparison["Absolute_Error"] = (
    comparison["Actual_Years"] - comparison["Predicted_Years"]
).abs()

print("\n【正解と予測の比較：先頭10件】")
print(comparison.head(10).round(2))


# =============================================================================
# 8. 正解値と予測値をグラフで比較する
# =============================================================================

figure, axis = plt.subplots(figsize=(7, 6))

axis.scatter(
    y_test,
    predicted_years,
    color="steelblue",
    alpha=0.75,
    edgecolor="white",
    label="Test samples",
)

# グラフ内の最小値と最大値を求め、理想的な予測を示す対角線を引きます。
lower_limit = min(y_test.min(), predicted_years.min())
upper_limit = max(y_test.max(), predicted_years.max())
axis.plot(
    [lower_limit, upper_limit],
    [lower_limit, upper_limit],
    color="crimson",
    linestyle="--",
    label="Perfect prediction",
)

# 点が対角線に近いほど、予測値が正解値に近いことを表します。
axis.set_title("Material Durability: Actual vs Predicted")
axis.set_xlabel("Actual durability (years)")
axis.set_ylabel("Predicted durability (years)")
axis.legend()
axis.grid(alpha=0.25)

figure.tight_layout()
plt.show()


print("\n注意：予測は候補選定の参考値です。最終判断には実際の耐久試験が必要です。")
print("学習データの範囲から大きく外れた材料配合への予測は避けてください。")
