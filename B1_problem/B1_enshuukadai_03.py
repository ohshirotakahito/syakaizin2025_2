# -*- coding: utf-8 -*-
"""
演習：品質検査CSVを安全に読み込む

【想定する場面】
品質検査で測定した吸光度データ（CSVファイル）を読み込んで分析したい。
ただし、演習を配布する環境によってはCSVファイルが手元にないこともある。
ファイルがない場合でも演習を進められるよう、その場でデモ用のCSVを
作ってから読み込む処理にする。

（課題）
1. 読み込みたいCSVファイルの場所（パス）を作る。
2. ファイルが存在するか確認し、存在しなければデモ用のCSVを作成する。
3. CSVファイルをpandasで読み込み、先頭数行・行数・列数・列名を表示する。
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd

file_path = Path(DATA_DIR / "absorbance_data.csv")

if not file_path.exists():
    # 配布用のCSVがない環境でも演習できるよう、練習用の小さなデータをその場で作ります。
    file_path.parent.mkdir(exist_ok=True)
    pd.DataFrame({
        "wavelength_nm": [400, 450, 500, 550, 600],
        "absorbance": [0.12, 0.35, 0.81, 0.46, 0.18],
    }).to_csv(file_path, index=False)
    print(f"演習用CSVを作成しました: {file_path}")

# TODO: file_pathのCSVを読み込み、DataFrame inspection を作ってください
# ヒント： pd.read_csv(file_path)
inspection = None

# TODO: 先頭5行を表示してください
# ヒント： inspection.head()

# TODO: 行数・列数を表示してください
# ヒント： inspection.shape[0]、inspection.shape[1]
print(f"行数={None}、列数={None}")

# TODO: 列名の一覧を表示してください
# ヒント： inspection.columns.tolist()
print("列名:", None)
