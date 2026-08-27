# -*- coding: utf-8 -*-
"""解答版：複数支店の月次売上Excelを統合し、集計・品質確認する。"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
import pandas as pd


def create_demo_workbook(file_path):
    """演習用ブックがない場合に、3支店分のシートを生成する。"""
    branch_data = {
        "Tokyo": [["2026-07-01", "Coffee", 120, 48000],
                  ["2026-07-01", "Tea", 85, 34000],
                  ["2026-07-02", "Coffee", 135, 54000]],
        "Osaka": [["2026-07-01", "Coffee", 95, 38000],
                  ["2026-07-01", "Tea", 110, 44000],
                  ["2026-07-02", "Coffee", 105, 42000]],
        "Fukuoka": [["2026-07-01", "Coffee", 70, 28000],
                    ["2026-07-01", "Tea", 78, 31200],
                    ["2026-07-02", "Coffee", 82, 32800]],
    }
    with pd.ExcelWriter(file_path) as writer:
        for branch, rows in branch_data.items():
            pd.DataFrame(rows, columns=["date", "product", "units", "sales_yen"]).to_excel(
                writer, sheet_name=branch, index=False
            )


def read_branch_sales(file_path):
    """全シートを読み、支店名を追加して1つの表へ統合する。"""
    required_columns = {"date", "product", "units", "sales_yen"}
    workbook = pd.ExcelFile(file_path)
    frames = []

    for sheet_name in workbook.sheet_names:
        sheet = workbook.parse(sheet_name)
        missing = required_columns - set(sheet.columns)
        if missing:
            raise ValueError(f"{sheet_name}シートに不足列があります: {sorted(missing)}")
        sheet["branch"] = sheet_name
        frames.append(sheet)

    combined = pd.concat(frames, ignore_index=True)
    combined["date"] = pd.to_datetime(combined["date"], errors="raise")
    return combined


data_directory = Path(DATA_DIR)
data_directory.mkdir(exist_ok=True)
workbook_path = data_directory / "branch_sales_demo.xlsx"
if not workbook_path.exists():
    create_demo_workbook(workbook_path)

sales = read_branch_sales(workbook_path)
print("【統合データ】")
print(sales)

# 支店別・商品別に売上と販売数を集計します。
summary = sales.groupby(["branch", "product"], as_index=False).agg(
    total_units=("units", "sum"),
    total_sales_yen=("sales_yen", "sum"),
)
print("\n【支店・商品別集計】")
print(summary)

# 集計結果を別Excelへ出力します。
output_path = data_directory / "branch_sales_summary.xlsx"
with pd.ExcelWriter(output_path) as writer:
    sales.to_excel(writer, sheet_name="Combined data", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)
print(f"\n集計ファイル: {output_path}")

