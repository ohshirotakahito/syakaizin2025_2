# -*- coding: utf-8 -*-
"""
演習：ディープニューラルネットワークを使用した新規材料の耐久度予測

【目的】
ディープニューラルネットワークを使用して、材料A、B、Cの混合比率に
基づいて新規材料の耐久度を予測する。

【手順】
1. データセットを読み込み、特徴量とターゲットを選択する。
2. データを標準化し、訓練データとテストデータに分割する。
3. ディープニューラルネットワークモデルを構築し、訓練する。
4. モデルを評価し、平均二乗誤差（MSE）を計算する。
5. 学習済みモデルとスケーラーを使用して、任意の混合比率から予測された耐久度を算出する。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data_path = DATA_DIR / "material_science_dataset1.csv"

if not data_path.exists():
    print(f"データが見つからないため、演習用の模擬データを作成します: {data_path}")
    data_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    n = 300

    ratios = rng.dirichlet([2, 2, 2], size=n) * 100
    ratio_a, ratio_b, ratio_c = ratios[:, 0], ratios[:, 1], ratios[:, 2]

    tensile_strength = rng.normal(50, 10, n)
    thermal_resistance = rng.normal(120, 20, n)
    elastic_modulus = rng.normal(3.0, 0.5, n)
    hardness = rng.normal(5, 1, n)
    corrosion_resistance = rng.integers(1, 11, n)
    electrical_conductivity = rng.normal(1e-3, 5e-4, n)
    density = rng.normal(1.2, 0.15, n)

    durability = (
        5
        + 0.04 * ratio_a + 0.07 * ratio_b + 0.02 * ratio_c
        + 0.03 * tensile_strength + 0.01 * thermal_resistance
        + 0.5 * elastic_modulus + 0.3 * corrosion_resistance
        + rng.normal(0, 1.0, n)
    )
    durability = np.clip(durability, 1, None)

    pd.DataFrame({
        "Existing_Durability_Years": durability,
        "Mixture_Ratio_A_Percent": ratio_a,
        "Mixture_Ratio_B_Percent": ratio_b,
        "Mixture_Ratio_C_Percent": ratio_c,
        "Tensile_Strength_MPa": tensile_strength,
        "Thermal_Resistance_C": thermal_resistance,
        "Elastic_Modulus_GPa": elastic_modulus,
        "Hardness_Mohs": hardness,
        "Corrosion_Resistance_Scale": corrosion_resistance,
        "Electrical_Conductivity_Sm": electrical_conductivity,
        "Density_g_cm3": density,
    }).to_csv(data_path, index=False)

df = pd.read_csv(data_path)

features = df.drop(['Existing_Durability_Years'], axis=1)
target = df['Existing_Durability_Years']

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=0
)

# TODO: StandardScalerとMLPRegressorをmake_pipeline()で組み合わせ、学習させてください
# ヒント： MLPRegressor(hidden_layer_sizes=(64, 32), early_stopping=True,
#                      max_iter=2000, random_state=42)
model = None

# TODO: model.predict()でX_testを予測してください
test_prediction = np.full(len(y_test), y_train.mean())  # 仮実装（平均値で予測）

print(f"Mean Squared Error: {mean_squared_error(y_test, test_prediction):.3f}")
print(f"R2: {r2_score(y_test, test_prediction):.3f}")


def predict_durability(model, mixture_ratios, original_columns, reference_features):
    """混合比率（辞書）から、モデルによる予測耐久年数を返す。"""
    mixture_df = pd.DataFrame([mixture_ratios])
    for col in original_columns:
        if col not in mixture_df.columns:
            mixture_df[col] = reference_features[col].mean()
    mixture_df = mixture_df[original_columns]

    if model is None:
        return float('nan')  # モデル未実装の間の仮の戻り値
    predicted_durability = model.predict(mixture_df)[0]
    return predicted_durability


mixture_ratios = {'Mixture_Ratio_A_Percent': 10, 'Mixture_Ratio_B_Percent': 30, 'Mixture_Ratio_C_Percent': 30}

predicted_durability = predict_durability(model, mixture_ratios, features.columns, features)
print(f"Predicted Durability: {predicted_durability}")
