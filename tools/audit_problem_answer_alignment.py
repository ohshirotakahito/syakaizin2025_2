"""Audit whether each problem describes the operations used by its answer."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
GROUPS = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "Other"]
GENERIC_NAMES = {
    "i", "j", "x", "y", "ax", "fig", "data", "df", "model", "result", "results",
    "file", "path", "value", "values", "index", "row", "col", "column", "columns",
}
GENERIC_CALLS = {"print", "len", "range", "str", "int", "float", "list", "dict", "set", "tuple"}


@dataclass
class Audit:
    answer: Path
    problem: Path
    required: set[str]
    present: set[str]

    @property
    def missing(self) -> set[str]:
        return self.required - self.present

    @property
    def coverage(self) -> float:
        return len(self.present) / len(self.required) if self.required else 1.0


def normalized(text: str) -> str:
    return re.sub(r"[^0-9a-zA-Z_./%]+", " ", text).lower()


def answer_terms(source: str) -> set[str]:
    tree = ast.parse(source)
    terms: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            terms.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if len(node.id) >= 3 and node.id.lower() not in GENERIC_NAMES:
                terms.add(node.id)
        elif isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name and len(name) >= 3 and name.lower() not in GENERIC_CALLS:
                terms.add(name)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value.strip()
            if (".csv" in value.lower() or ".xlsx" in value.lower() or
                    ".png" in value.lower() or re.fullmatch(r"[A-Za-z][A-Za-z0-9_ /%.-]{3,}", value)):
                terms.add(value)
    return {term for term in terms if not term.startswith("_")}


def pairs() -> list[tuple[Path, Path]]:
    found = []
    for group in GROUPS:
        for answer in sorted((ROOT / f"{group}_Ans").glob("*.py")):
            base = answer.stem.removesuffix("_Ans")
            found.append((answer, ROOT / f"{group}_problem" / f"{base}_problem.py"))
    return found


def audit(answer: Path, problem: Path) -> Audit:
    required = answer_terms(answer.read_text(encoding="utf-8"))
    problem_words = normalized(problem.read_text(encoding="utf-8"))
    present = {term for term in required if normalized(term).strip() in problem_words}
    return Audit(answer, problem, required, present)


def main() -> None:
    audits = [audit(answer, problem) for answer, problem in pairs()]
    failed = [item for item in audits if item.coverage < 0.70]
    for item in sorted(audits, key=lambda value: value.coverage):
        relative = item.problem.relative_to(ROOT)
        print(f"{item.coverage:6.1%} {relative} missing={', '.join(sorted(item.missing)[:8])}")
    print(f"\nAudited: {len(audits)}, below 70%: {len(failed)}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
