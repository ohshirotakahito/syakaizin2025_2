# -*- coding: utf-8 -*-
"""全問題版に誘導・穴埋め・選択・考察の必須セクションを保証する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
problem_files = sorted(
    file
    for directory in ROOT.iterdir()
    if directory.is_dir() and directory.name.endswith("_problem")
    for file in directory.glob("*.py")
)

updated = 0
for path in problem_files:
    text = path.read_text(encoding="utf-8")
    additions = []

    if "TODO" not in text:
        additions.extend([
            "",
            "# 【実装欄（穴埋め）】",
            "# TODO：上の各指示に対応するコードを、処理順が分かるように記入してください。",
        ])

    if "選択" not in text:
        additions.extend([
            "",
            "# 【選択問題】実行結果が想定と異なる場合、最初に行う確認として適切なのはどれですか。",
            "# A. 入力データ・単位・列名とエラーメッセージを確認する",
            "# B. 根拠なくすべてのデータを削除する",
            "# C. 結果を確認せず、そのまま業務判断に使う",
            "# 答え：",
        ])

    if "考察" not in text:
        additions.extend([
            "",
            "# 【考察問題】この結果を実務で利用する前に、確認すべき前提・データ品質・",
            "# 判断上の限界を、自分の言葉で1つ以上説明してください。",
            "# 答え：",
        ])

    if additions:
        path.write_text(text.rstrip() + "\n" + "\n".join(additions) + "\n", encoding="utf-8")
        updated += 1

print(f"Checked {len(problem_files)} problem files; updated {updated}")
