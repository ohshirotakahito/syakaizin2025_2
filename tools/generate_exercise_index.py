# -*- coding: utf-8 -*-
"""問題版・解答版フォルダから教材索引を生成する保守用スクリプト。"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent


def title_from_problem(path: Path) -> str:
    """問題版ファイルの冒頭から人が読める題名を取得する。"""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"問題版[：:](.+)", text)
    if match:
        return match.group(1).strip().rstrip("。\"")
    return path.stem.replace("_problem", "").replace("_", " ")


answer_directories = sorted(
    path for path in ROOT.iterdir() if path.is_dir() and path.name.endswith("_Ans")
)
rows_by_group = {}
unmatched = []

for answer_directory in answer_directories:
    group = answer_directory.name.removesuffix("_Ans")
    problem_directory = ROOT / f"{group}_problem"
    rows = []
    for answer_path in sorted(answer_directory.glob("*.py")):
        base_name = answer_path.stem.removesuffix("_Ans")
        problem_path = problem_directory / f"{base_name}_problem.py"
        if not problem_path.exists():
            unmatched.append(str(answer_path.relative_to(ROOT)))
            continue
        rows.append((base_name, title_from_problem(problem_path), problem_path, answer_path))
    rows_by_group[group] = rows

total_pairs = sum(len(rows) for rows in rows_by_group.values())
lines = [
    "# Python演習教材 索引",
    "",
    "各教材は、誘導・穴埋め・選択・考察を含む問題版と、コメント付き完成コードの解答版に分かれています。",
    "",
    f"- 教材ペア数: **{total_pairs}**",
    "- 問題版: `*_problem`フォルダ",
    "- 解答版: `*_Ans`フォルダ",
    "- 実行基準ディレクトリ: リポジトリ直下",
    "",
    "## 推奨環境",
    "",
    "Python 3.14で検証しています。主なライブラリはNumPy、Pandas、Matplotlib、SciPy、",
    "scikit-learn、Seaborn、OpenCV、Pillow、openpyxlです。グラフを表示する解答では、",
    "実行後にグラフウィンドウを閉じると処理が終了します。",
    "",
    "## 教材構成",
    "",
    "| 系列 | ペア数 | 主な内容 |",
    "|---|---:|---|",
]

descriptions = {
    "A1": "変数、型、演算、条件分岐、反復",
    "A2": "リスト、タプル、辞書、集合",
    "A3": "関数、クラス、文字列、ファイル、業務ツール",
    "B1": "NumPy・Pandasによる表データ操作",
    "B2": "業務データの可視化",
    "B3": "長期気候データ分析",
    "C1": "数値計算、検量線、希釈、回帰",
    "C2": "統計検定、前処理、画像・スペクトル解析",
    "C3": "科学・材料データの機械学習とシミュレーション",
    "D1": "PCA、クラスタリング、分類、回帰の90分演習",
    "Other": "科学計測、画像、時系列、機械学習の発展教材",
}

for group, rows in rows_by_group.items():
    lines.append(f"| {group} | {len(rows)} | {descriptions.get(group, '演習')} |")

for group, rows in rows_by_group.items():
    lines.extend(["", f"## {group} 系", "", "| No. | テーマ | 問題版 | 解答版 |", "|---:|---|---|---|"])
    for number, (base, title, problem_path, answer_path) in enumerate(rows, start=1):
        problem_link = problem_path.relative_to(ROOT).as_posix()
        answer_link = answer_path.relative_to(ROOT).as_posix()
        lines.append(
            f"| {number} | {title} | [問題]({problem_link}) | [解答]({answer_link}) |"
        )

lines.extend([
    "",
    "## 使い方",
    "",
    "1. 問題版を開き、TODO部分へコードを書きます。",
    "2. 選択問題と考察問題へ、自分の言葉で回答します。",
    "3. 実行結果を確認した後、対応する解答版と比較します。",
    "4. 解答を写すだけでなく、データや条件を変えて結果の変化を確認します。",
    "",
    "## 注意",
    "",
    "医療、品質、安全、融資などを題材にしたコードは学習用です。実際の診断・品質保証・",
    "安全判断・顧客への不利益な意思決定へ、そのまま使用しないでください。",
])

if unmatched:
    lines.extend(["", "## 対応する問題版がない解答", ""])
    lines.extend(f"- `{path}`" for path in unmatched)

(ROOT / "EXERCISE_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Generated EXERCISE_INDEX.md with {total_pairs} pairs")
if unmatched:
    print(f"Unmatched answers: {len(unmatched)}")
