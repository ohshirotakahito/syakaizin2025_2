# -*- coding: utf-8 -*-
"""
演習：検査データへ判定列を追加しCSVへ出力する（解説付き解答版）

【想定する場面】
品質検査の測定値（吸光度）について、「平均以上かどうか」を一目で
分かるようにしたい。判定結果を新しい列として追加し、別のCSVファイルへ
保存して他の担当者と共有できるようにする。

（課題）
1. 検査データのCSVを読み込む（なければデモ用データを作る）。
2. 数値列の平均値を求め、各行がその平均以上かどうかを判定する列を追加する。
3. 判定を追加した表を、新しいCSVファイルとして保存する。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
import pandas as pd

input_path = Path(DATA_DIR / "absorbance_data.csv")
if not input_path.exists():
    input_path.parent.mkdir(exist_ok=True)
    pd.DataFrame({
        "wavelength_nm": [400, 450, 500, 550, 600],
        "absorbance": [0.12, 0.35, 0.81, 0.46, 0.18],
    }).to_csv(input_path, index=False)

data = pd.read_csv(input_path)

# select_dtypes("number") は、表の中から数値型（int, floatなど）の列だけを
# 選び出します。今回は複数の数値列があっても構わないよう、
# その最初の1列（[0]）を「検査値」として扱います。
numeric_column = data.select_dtypes("number").columns[0]

# data[numeric_column] >= data[numeric_column].mean() は、
# 「その列の各値が、その列の平均以上かどうか」を1行ずつTrue/Falseで判定します。
# 結果をそのまま新しい列 "above_average" として表へ追加できます。
data["above_average"] = data[numeric_column] >= data[numeric_column].mean()

output_path = Path(DATA_DIR / "absorbance_checked.csv")

# to_csv()でCSVファイルへ保存します。
# encoding="utf-8-sig" にすると、ExcelでCSVを開いたときに日本語が
# 文字化けしにくくなります（先頭に「BOM」という目印が付くためです）。
data.to_csv(output_path, index=False, encoding="utf-8-sig")

print(data.head())
print("保存先:", output_path)

# 【ポイント】
# ・比較演算子（>=, ==など）をpandasの列に対して使うと、True/Falseの列が作れます。
# ・to_csv()で保存する際は、日本語を含む場合はencoding="utf-8-sig"にしておくと安心です。
