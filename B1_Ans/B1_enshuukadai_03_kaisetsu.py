# -*- coding: utf-8 -*-
"""
演習：品質検査CSVを安全に読み込む（解説付き解答版）

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

# Path(__file__)は「このファイル自身の場所」を表します。
# .resolve()で絶対パス（省略のないフルパス）にし、.parent.parentで
# 2つ上の階層のフォルダ（プロジェクトの一番上のフォルダを想定）へ移動します。
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 「/」でフォルダ名やファイル名をつなげると、OSの違い（Windowsは\、Macは/）を
# 気にせずファイルの場所を組み立てられます。
DATA_DIR = PROJECT_ROOT / "data"

import pandas as pd

file_path = Path(DATA_DIR / "absorbance_data.csv")

# .exists() は、そのパスにファイル（またはフォルダ）が実際にあるかをTrue/Falseで返します。
if not file_path.exists():
    # 配布用のCSVがない環境でも演習できるよう、練習用の小さなデータをその場で作ります。
    # parent.mkdir(exist_ok=True) は、保存先フォルダがまだなければ作る命令です。
    # exist_ok=True にしておくと、すでにフォルダがあってもエラーになりません。
    file_path.parent.mkdir(exist_ok=True)

    pd.DataFrame({
        "wavelength_nm": [400, 450, 500, 550, 600],
        "absorbance": [0.12, 0.35, 0.81, 0.46, 0.18],
    }).to_csv(file_path, index=False)
    print(f"演習用CSVを作成しました: {file_path}")

# pd.read_csv() で、CSVファイルの中身をDataFrame（表）として読み込みます。
inspection = pd.read_csv(file_path)

# .head() は表の先頭5行だけを表示します。行数が多い表の中身をざっと
# 確認したいときによく使います。
print(inspection.head())

# .shape は表の (行数, 列数) をタプルで返します。
print(f"行数={inspection.shape[0]}、列数={inspection.shape[1]}")

# .columns で列名の一覧を確認できます。
print("列名:", inspection.columns.tolist())

# 【ポイント】
# ・「ファイルがなければ作る」処理を入れておくと、環境が違っても演習が止まりません。
# ・read_csv()で読んだ直後は、必ずhead()やshapeで中身と大きさを確認する習慣が大切です。
