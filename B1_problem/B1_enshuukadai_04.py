# -*- coding: utf-8 -*-
"""
演習：検査データへ判定列を追加しCSVへ出力する

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

# TODO: 数値型の列のうち最初の1列の列名をnumeric_columnとして取り出してください
# ヒント： data.select_dtypes("number").columns[0]
numeric_column = None

# TODO: numeric_column列の値が、その列の平均以上かどうかを判定する
#       "above_average"列をdataへ追加してください
# ヒント： data[numeric_column] >= data[numeric_column].mean()
data["above_average"] = None

output_path = Path(DATA_DIR / "absorbance_checked.csv")

# TODO: dataをoutput_pathへCSVとして保存してください（日本語対応のためutf-8-sig指定）
# ヒント： data.to_csv(output_path, index=False, encoding="utf-8-sig")

print(data.head())
print("保存先:", output_path)
