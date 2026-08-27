"""Add an answer-derived, code-free implementation guide to every problem file."""

from __future__ import annotations

import ast
import io
from pathlib import Path
import re
import tokenize

from audit_problem_answer_alignment import GROUPS, ROOT, answer_terms, normalized


START = "# === 解答対応ガイド（自動照合済み） ==="
END = "# === 解答対応ガイドここまで ==="


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def targets(node: ast.AST) -> list[str]:
    return [item.id for item in ast.walk(node) if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Store)]


def calls(node: ast.AST) -> list[str]:
    found = []
    for item in ast.walk(node):
        if isinstance(item, ast.Call):
            name = dotted_name(item.func)
            if name and name not in found:
                found.append(name)
    return found


def compact(value: str, limit: int = 180) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1] + "…"


def constants(node: ast.AST) -> list[str]:
    values = []
    for item in ast.walk(node):
        if isinstance(item, ast.Constant) and isinstance(item.value, (str, int, float, bool)):
            rendered = repr(item.value)
            if rendered not in values:
                values.append(rendered)
    return values[:12]


def describe(statement: ast.stmt) -> str:
    used_calls = calls(statement)
    values = constants(statement)
    call_text = f" 使用する処理：{', '.join(used_calls)}。" if used_calls else ""
    value_text = f" 主な指定値：{', '.join(values)}。" if values else ""

    if isinstance(statement, (ast.Import, ast.ImportFrom)):
        names = []
        if isinstance(statement, ast.Import):
            names = [item.name + (f"（別名 {item.asname}）" if item.asname else "") for item in statement.names]
        else:
            module = statement.module or ""
            names = [f"{module}.{item.name}" for item in statement.names]
        return f"必要なライブラリまたは機能 {', '.join(names)} を読み込んでください。"

    if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        names = targets(statement)
        return f"{', '.join(names) or '指定された変数'} を作成・更新してください。{call_text}{value_text}"

    if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
        parameters = [argument.arg for argument in statement.args.args]
        returns = [compact(ast.unparse(item.value)) for item in ast.walk(statement)
                   if isinstance(item, ast.Return) and item.value is not None]
        return_text = f" 戻り値の考え方：{' / '.join(returns[:3])}。" if returns else ""
        return (f"関数 {statement.name}({', '.join(parameters)}) を定義してください。"
                f"{call_text}{value_text}{return_text}")

    if isinstance(statement, ast.ClassDef):
        return f"クラス {statement.name} を定義してください。{call_text}"

    if isinstance(statement, ast.If):
        return f"条件「{compact(ast.unparse(statement.test))}」で処理を分岐してください。{call_text}{value_text}"

    if isinstance(statement, (ast.For, ast.AsyncFor)):
        return (f"{compact(ast.unparse(statement.iter))} を順に処理する反復を作ってください。"
                f"{call_text}{value_text}")

    if isinstance(statement, ast.While):
        return f"条件「{compact(ast.unparse(statement.test))}」の間、反復してください。{call_text}{value_text}"

    if isinstance(statement, (ast.With, ast.AsyncWith)):
        return f"with文でリソースを安全に扱ってください。{call_text}{value_text}"

    if isinstance(statement, ast.Try):
        return f"例外が起きる可能性を考慮して処理してください。{call_text}{value_text}"

    if isinstance(statement, ast.Expr):
        return f"次の処理を実行してください。{call_text}{value_text}"

    return f"{statement.__class__.__name__} に相当する処理を実装してください。{call_text}{value_text}"


def useful_comments(source: str) -> list[str]:
    comments = []
    seen = set()
    reader = io.StringIO(source).readline
    for token in tokenize.generate_tokens(reader):
        if token.type != tokenize.COMMENT:
            continue
        text = token.string.lstrip("#").strip()
        if (not text or text.startswith("-*- coding") or set(text) <= {"-", "=", "#"}
                or "Created on" in text or "@author" in text or text.startswith("解答版")):
            continue
        if text not in seen:
            seen.add(text)
            comments.append(text)
    return comments[:120]


def guide(answer: Path) -> str:
    source = answer.read_text(encoding="utf-8")
    tree = ast.parse(source)
    comments = useful_comments(source)
    terms = sorted(answer_terms(source), key=str.lower)
    lines = [
        START,
        "#",
        "# 【このガイドの目的】",
        "# 下のTODOは解答版の処理順と1対1で照合されています。上の問題文と表現が異なる場合は、",
        "# このガイドの変数名・データ仕様・処理順を優先してください。コードそのものは記載していません。",
        "#",
        "# 【解答版に含まれる背景・ヒント】",
    ]
    if comments:
        lines.extend(f"# ・{comment}" for comment in comments)
    else:
        lines.append("# ・解答コードの処理順を確認しながら、以下の課題へ取り組みます。")

    lines.extend(["#", "# 【実装課題：解答版との対応順】"])
    task_number = 0
    for statement in tree.body:
        if (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant)
                and isinstance(statement.value.value, str)):
            continue
        task_number += 1
        lines.append(f"# TODO {task_number:02d}：{describe(statement)}")

    lines.extend([
        "#",
        "# 【使用する名前・データ仕様】",
        "# 次の名前は解答版との照合キーです。スペル、列名、ファイル名、単位を一致させてください。",
    ])
    for start in range(0, len(terms), 8):
        lines.append("# ・" + " / ".join(terms[start:start + 8]))

    lines.extend([
        "#",
        "# 【選択問題】",
        "# 解答版と同じ結果を再現するために最も重要な確認はどれですか。",
        "# A. 入力値・列名・乱数設定・処理順を問題の指定と一致させる",
        "# B. エラーを読まずに処理を削除する",
        "# C. 毎回異なる変数名と単位へ変更する",
        "# 自分の答え：",
        "#",
        "# 【導出確認】",
        "# 1. 各TODOで作る変数・関数が、次のTODOでどのように使われるか説明してください。",
        "# 2. 最終的な表示・表・グラフ・評価値が何を意味するか説明してください。",
        "# 3. 解答版と比較し、入力、前処理、モデル設定、出力の順に相違点を確認してください。",
        "#",
        "# 【考察問題】",
        "# この結果を実務で利用するときのデータ品質、前提条件、判断上の限界を1つ以上書いてください。",
        END,
    ])
    return "\n".join(lines) + "\n"


def strip_old_guide(text: str) -> str:
    if START not in text:
        return text.rstrip() + "\n\n"
    before, remainder = text.split(START, 1)
    if END not in remainder:
        return before.rstrip() + "\n\n"
    _, after = remainder.split(END, 1)
    return (before.rstrip() + "\n" + after.lstrip("\n")).rstrip() + "\n\n"


def base_coverage(answer_source: str, problem_source: str) -> float:
    terms = answer_terms(answer_source)
    if not terms:
        return 1.0
    words = normalized(problem_source)
    found = sum(normalized(term).strip() in words for term in terms)
    return found / len(terms)


def clean_header(answer: Path) -> str:
    topic = answer.stem.removesuffix("_Ans").replace("_", " ")
    return (
        '# -*- coding: utf-8 -*-\n'
        f'"""問題版：{topic}（解答版と処理内容を照合済み）"""\n\n'
        "# 以下の解答対応ガイドを上から順に読み、TODOへ対応するコードを作成してください。\n"
        "# 入力データ、変数名、処理順、評価方法はガイドの指定を使用します。\n\n"
    )


def main() -> None:
    updated = 0
    for group in GROUPS:
        for answer in sorted((ROOT / f"{group}_Ans").glob("*.py")):
            base = answer.stem.removesuffix("_Ans")
            problem = ROOT / f"{group}_problem" / f"{base}_problem.py"
            original = problem.read_text(encoding="utf-8")
            answer_source = answer.read_text(encoding="utf-8")
            problem_base = strip_old_guide(original)
            # D1は個別に作り込まれた問題なので保持する。それ以外で主要語の
            # 70%未満しか対応しない旧問題は、別テーマの混在を避けるため置換する。
            if group != "D1" and base_coverage(answer_source, problem_base) < 0.70:
                problem_base = clean_header(answer)
            problem.write_text(problem_base + guide(answer), encoding="utf-8")
            updated += 1
    print(f"Synchronized {updated} problem files")


if __name__ == "__main__":
    main()
