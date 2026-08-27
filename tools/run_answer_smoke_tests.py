# -*- coding: utf-8 -*-
"""全解答版を非対話グラフ環境で実行するスモークテスト。"""

from pathlib import Path
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
answer_directories = sorted(
    path for path in ROOT.iterdir() if path.is_dir() and path.name.endswith("_Ans")
)
answer_files = sorted(
    file for directory in answer_directories for file in directory.glob("*.py")
)

environment = os.environ.copy()
environment["MPLBACKEND"] = "Agg"
environment["PYTHONIOENCODING"] = "utf-8"
test_input = "1\n2\n+\nいいえ\n"
failures = []

for number, path in enumerate(answer_files, start=1):
    relative = path.relative_to(ROOT)
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            # IDEやPowerShellで解答フォルダから起動する条件を再現する。
            cwd=path.parent,
            env=environment,
            input=test_input,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        failures.append((str(relative), "timeout after 60 seconds"))
        print(f"FAIL {number:03d}/{len(answer_files)} {relative}: timeout")
        continue

    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip().splitlines()
        failures.append((str(relative), message[-1] if message else "unknown error"))
        print(f"FAIL {number:03d}/{len(answer_files)} {relative}")
    else:
        print(f"OK   {number:03d}/{len(answer_files)} {relative}")

if failures:
    print("\nSMOKE TEST FAILED")
    for path, message in failures:
        print(f"- {path}: {message}")
    sys.exit(1)

print(f"\nSMOKE TEST PASSED: {len(answer_files)} answer files")
