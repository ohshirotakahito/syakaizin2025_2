# -*- coding: utf-8 -*-
"""教材ペア数、対応関係、問題版の必須要素を検証する。"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
GROUPS = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "Other"]

# 全92本を数えた時点ではD1_02〜08は既に分離済みだったため、今回対象はD1_01の1本です。
ORIGINAL_SCOPE_COUNTS = {
    "A1": 1, "A2": 1, "A3": 10,
    "B1": 10, "B2": 11, "B3": 1,
    "C1": 5, "C2": 16, "C3": 10,
    "D1": 1, "Other": 26,
}

errors = []
all_pairs = 0

for group in GROUPS:
    answer_directory = ROOT / f"{group}_Ans"
    problem_directory = ROOT / f"{group}_problem"
    answers = {path.stem.removesuffix("_Ans"): path for path in answer_directory.glob("*.py")}
    problems = {path.stem.removesuffix("_problem"): path for path in problem_directory.glob("*.py")}
    all_pairs += len(answers)

    if answers.keys() != problems.keys():
        errors.append(
            f"{group}: pair mismatch; answer-only={sorted(answers.keys()-problems.keys())}, "
            f"problem-only={sorted(problems.keys()-answers.keys())}"
        )

    for base_name, problem_path in problems.items():
        text = problem_path.read_text(encoding="utf-8")
        for required in ["TODO", "選択", "考察"]:
            if required not in text:
                errors.append(f"{problem_path.relative_to(ROOT)}: missing {required}")

    for base_name, answer_path in answers.items():
        text = answer_path.read_text(encoding="utf-8")
        if "解答版" not in text:
            errors.append(f"{answer_path.relative_to(ROOT)}: missing answer label")

root_python_files = sorted(ROOT.glob("*.py"))
if root_python_files:
    errors.append(f"Python files remain at repository root: {[p.name for p in root_python_files]}")

original_scope_total = sum(ORIGINAL_SCOPE_COUNTS.values())
if original_scope_total != 92:
    errors.append(f"Original scope count is {original_scope_total}, expected 92")

if all_pairs != 99:
    errors.append(f"Total pair count is {all_pairs}, expected 99 (92 target + 7 prior D1 pairs)")

if not (ROOT / "EXERCISE_INDEX.md").exists():
    errors.append("EXERCISE_INDEX.md is missing")

if errors:
    print("VERIFICATION FAILED")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print("VERIFICATION PASSED")
print(f"Original requested scope: {original_scope_total} files")
print(f"Available exercise pairs: {all_pairs} (includes 7 prior D1 pairs)")
print("Every pair has a problem and answer file; every problem has TODO, selection, and consideration sections.")
