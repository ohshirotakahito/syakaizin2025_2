"""Make data paths in answer scripts independent of the current directory."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent


def answer_files() -> list[Path]:
    return sorted(path for folder in ROOT.glob("*_Ans") for path in folder.glob("*.py"))


def uses_data_path(source: str) -> bool:
    return bool(re.search(r"(['\"])data(?:[/\\][^'\"]*)?\1", source))


def convert_data_paths(source: str) -> str:
    pattern = re.compile(r"(['\"])data(?:[/\\]([^'\"]*))?\1")

    def replacement(match: re.Match[str]) -> str:
        relative = (match.group(2) or "").replace("\\", "/")
        if relative:
            return f'DATA_DIR / "{relative}"'
        return "DATA_DIR"

    return pattern.sub(replacement, source)


def add_path_setup(source: str) -> str:
    setup = 'PROJECT_ROOT = Path(__file__).resolve().parent.parent\nDATA_DIR = PROJECT_ROOT / "data"\n'
    if "from pathlib import Path" in source:
        return source.replace("from pathlib import Path\n", f"from pathlib import Path\n\n{setup}", 1)
    return f"from pathlib import Path\n\n{setup}\n{source}"


def main() -> None:
    changed = []
    for path in answer_files():
        source = path.read_text(encoding="utf-8")
        if not uses_data_path(source) or "DATA_DIR = PROJECT_ROOT" in source:
            continue
        updated = add_path_setup(convert_data_paths(source))
        path.write_text(updated, encoding="utf-8")
        changed.append(path.relative_to(ROOT))

    print(f"Updated {len(changed)} answer files")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
