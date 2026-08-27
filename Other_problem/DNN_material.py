# -*- coding: utf-8 -*-
"""
演習：材料特性から耐久年数をニューラルネットワークで予測する

【想定する場面】
材料メーカーで、新しい材料候補の耐久試験には長い時間が必要です。そこで、
過去に試験した材料の物性値と配合比率から、耐久年数の目安を予測します。

ここではscikit-learnのMLPRegressorを使います。MLPは複数の層で数値の関係を
学習するニューラルネットワークです。「DNN」という言葉は一般に層の深い
ニューラルネットワークを指しますが、この演習では学習しやすい小規模な
多層パーセプトロンを使用します。

※ 実行するには data/material_science_dataset3.csv（無ければ dataset1.csv）
   を用意してください。
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# =============================================================================
# 1. 材料データを読み込む
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

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

target_column = "Existing_Durability_Years"
features = materials.drop(columns=[target_column])
target = materials[target_column]

print("\n【特徴量】")
for column_name in features.columns:
    print(f"・{column_name}")


# =============================================================================
# 3. 学習用データとテスト用データに分ける
# =============================================================================

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

# TODO: StandardScalerとMLPRegressorをmake_pipeline()で組み合わせてください
# ヒント：
#   MLPRegressor(hidden_layer_sizes=(32, 16), solver="lbfgs",
#                max_iter=3000, random_state=42)
model = None


# =============================================================================
# 5. モデルを学習し、未知データを予測する
# =============================================================================

# TODO: model.fit()で学習し、model.predict()でX_testを予測してください
predicted_years = None


# =============================================================================
# 6. 予測性能を数値で評価する
# =============================================================================

mae = mean_absolute_error(y_test, predicted_years)
mse = mean_squared_error(y_test, predicted_years)
r2 = r2_score(y_test, predicted_years)

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

lower_limit = min(y_test.min(), predicted_years.min())
upper_limit = max(y_test.max(), predicted_years.max())
axis.plot(
    [lower_limit, upper_limit],
    [lower_limit, upper_limit],
    color="crimson",
    linestyle="--",
    label="Perfect prediction",
)

axis.set_title("Material Durability: Actual vs Predicted")
axis.set_xlabel("Actual durability (years)")
axis.set_ylabel("Predicted durability (years)")
axis.legend()
axis.grid(alpha=0.25)

figure.tight_layout()
plt.show()


print("\n注意：予測は候補選定の参考値です。最終判断には実際の耐久試験が必要です。")
print("学習データの範囲から大きく外れた材料配合への予測は避けてください。")
