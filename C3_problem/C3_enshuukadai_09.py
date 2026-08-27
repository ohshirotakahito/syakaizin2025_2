# -*- coding: utf-8 -*-
"""
演習：ランダムフォレストを使用した新規材料の耐久度予測

【背景】
材料A、B、Cの混合比率と各種特性から、材料の耐久性を予測し、
耐久性を最大化する混合比率を求める。

【手順】
1. データセットを分析し、各特性が耐久性にどう影響するかを理解する。
2. ランダムフォレストで耐久性に影響を与える要因を学習する。
3. 最適化アルゴリズムで、耐久性を最大化する混合比率を求める。
4. 最適な混合比率を用いて、新規材料の耐久度を予測する。

※ このファイルはTODOを埋める前でも最後まで実行できます。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from scipy.optimize import minimize

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

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=0)

# TODO: RandomForestRegressor(random_state=0)を作成し、学習させてください
model = RandomForestRegressor(random_state=0)
model.fit(X_train, np.full(len(y_train), y_train.mean()))  # 仮実装（平均だけを学習）

predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse:.3f}")


def optimize_mixture_ratio(x):
    """混合比率xに対する、モデル予測耐久性の符号を反転した値を返す。"""
    mixture_df = pd.DataFrame([x], columns=[
        'Mixture_Ratio_A_Percent', 'Mixture_Ratio_B_Percent', 'Mixture_Ratio_C_Percent'
    ])
    for col in features.columns:
        if col not in mixture_df.columns:
            mixture_df[col] = features[col].mean()
    mixture_df = mixture_df[features.columns]
    return -model.predict(mixture_df)[0]


constraints = ({'type': 'eq', 'fun': lambda x: 100 - sum(x)})

initial_guess = [10, 10, 10]
result = minimize(optimize_mixture_ratio, initial_guess, constraints=constraints,
                   bounds=[(0, 100), (0, 100), (0, 100)])
optimal_mixture = result.x

optimal_mixture_df = pd.DataFrame([optimal_mixture], columns=[
    'Mixture_Ratio_A_Percent', 'Mixture_Ratio_B_Percent', 'Mixture_Ratio_C_Percent'
])
for col in features.columns:
    if col not in optimal_mixture_df.columns:
        optimal_mixture_df[col] = features[col].mean()
optimal_mixture_df = optimal_mixture_df[features.columns]
predicted_durability = model.predict(optimal_mixture_df)[0]

print(f"Optimal Mixture Ratios: A: {optimal_mixture[0]:.2f}%, B: {optimal_mixture[1]:.2f}%, C: {optimal_mixture[2]:.2f}%")
print(f"Predicted Durability: {predicted_durability:.2f} years")
