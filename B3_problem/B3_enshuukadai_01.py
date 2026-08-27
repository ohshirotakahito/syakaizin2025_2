# -*- coding: utf-8 -*-
"""
演習：長期気候データの傾向・移動平均・相関を分析する

【課題の背景】
近年、気候変動は重要な環境問題となっています。この問題を理解するためには、
過去の気候データを分析し、長期的な傾向を把握することが重要です。

【課題】
1910年から2010年までの気温、太陽黒点、森林面積、工業生産高のデータを用いて、
以下の分析を行います。

1. データの読み込みと概観：
   提供されたCSVファイルからデータを読み込み、基本的な統計情報を確認する。
2. データの可視化：
   気温、太陽黒点、森林面積、工業生産高の時間に対する変化を可視化する。
   各変数の年間の変化傾向を把握するために、折れ線グラフを作成する。
3. データの相関分析：
   気温と他の変数（太陽黒点、森林面積、工業生産高）との相関を分析する。
   相関関係を可視化するために、ヒートマップを使用する。
4. 結論の導出：
   分析結果を基に、気温の長期的な傾向や他の変数との関連性について
   結論を導き出す。

【データセット】
Climate_Data.csv：1910年から2010年までの気温、太陽黒点、森林面積、
工業生産高を含むデータセット。

※ このファイルはTODOを埋める前でも最後まで実行できます。
   未実装の部分は0や仮の値になっているため、グラフやメッセージの内容は
   正しくありません。TODOを実装しながら、結果が正しく変わっていくことを
   確認してください。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# 1. データの読み込みと概観
# =============================================================================

file_path = Path(DATA_DIR / "Climate_Data.csv")

if not file_path.exists():
    # 配布用のCSVがない環境でも演習できるよう、練習用の模擬データをその場で作ります。
    print(f"気候データが見つからないため、演習用の模擬データを作成します: {file_path}")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    years = np.arange(1910, 2011)

    temperature = 13.5 + 0.008 * (years - 1910) + rng.normal(0, 0.3, years.size)
    sunspots = 50 + 40 * np.sin(2 * np.pi * (years - 1910) / 11) + rng.normal(0, 8, years.size)
    forest_area = 4200 - 3.0 * (years - 1910) + rng.normal(0, 15, years.size)
    industrial_output = 10 * np.exp(0.018 * (years - 1910)) + rng.normal(0, 5, years.size)

    pd.DataFrame({
        "Year": years,
        "Temperature": temperature,
        "Sunspots": sunspots,
        "Forest Area": forest_area,
        "Industrial Output": industrial_output,
    }).to_csv(file_path, index=False)

data = pd.read_csv(file_path)

# 必須列を検査すると、列名違いや不完全なファイルを早期発見できます。
required = {'Year', 'Temperature', 'Sunspots', 'Forest Area', 'Industrial Output'}
missing = required - set(data.columns)
if missing:
    raise ValueError(f"不足列: {sorted(missing)}")

# TODO: dataの基本統計量（件数・平均・標準偏差・最小最大など）を表示してください
# ヒント： data.describe()


# =============================================================================
# 2. 移動平均と長期傾向を計算する
# =============================================================================

# TODO: Temperature列の10年移動平均を求め、"Temperature 10Y Mean"列に入れてください
# ヒント： data['Temperature'].rolling(10, center=True).mean()
# 未実装の間はNaN（欠測値）で埋めておくので、下のグラフは線が表示されません。
data['Temperature 10Y Mean'] = np.nan

# TODO: np.polyfit()を使って、Year（年）とTemperature（気温）の関係を
#       1次式で近似したときの傾きslopeと切片interceptを求めてください
# ヒント： np.polyfit(data['Year'], data['Temperature'], 1)
# 未実装の間は0.0にしておくので、下のメッセージは「10年あたり0.000度」と表示されます。
slope, intercept = 0.0, 0.0

print(f"気温の線形傾向: 10年あたり{slope * 10:.3f}度")


# =============================================================================
# 3. 4つの変数を折れ線グラフで可視化する
# =============================================================================

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(data['Year'], data['Temperature'], label='Temperature')
plt.plot(data['Year'], data['Temperature 10Y Mean'], label='10-year mean', linewidth=2)
plt.xlabel('Year')
plt.ylabel('Temperature')
plt.title('Temperature Over Years')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(data['Year'], data['Sunspots'], label='Sunspots')
plt.xlabel('Year')
plt.ylabel('Sunspots')
plt.title('Sunspots Over Years')

plt.subplot(2, 2, 3)
plt.plot(data['Year'], data['Forest Area'], label='Forest Area')
plt.xlabel('Year')
plt.ylabel('Forest Area')
plt.title('Forest Area Over Years')

plt.subplot(2, 2, 4)
plt.plot(data['Year'], data['Industrial Output'], label='Industrial Output')
plt.xlabel('Year')
plt.ylabel('Industrial Output')
plt.title('Industrial Output Over Years')

plt.tight_layout()
plt.show()


# =============================================================================
# 4. 相関分析（気温と他の変数との関係を数値・ヒートマップで確認する）
# =============================================================================

# TODO: 数値列だけを選び、すべての数値列どうしの相関係数を求めた
#       correlation_matrixを作ってください
# ヒント： data.select_dtypes('number').corr()
# 未実装の間は、同じ形（同じ行・列名）のダミー行列を0で埋めて代わりに使います。
numeric_columns = data.select_dtypes('number').columns
correlation_matrix = pd.DataFrame(
    np.zeros((len(numeric_columns), len(numeric_columns))),
    index=numeric_columns,
    columns=numeric_columns,
)

sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Analysis')
plt.tight_layout()
plt.show()


# =============================================================================
# 5. 結論を導くうえでの注意
# =============================================================================

print('注意：相関は因果関係を証明しません。時系列では各変数が同時に')
print('増減するだけで高い相関になる場合もあり、追加検証が必要です。')
