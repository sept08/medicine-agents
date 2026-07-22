from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Iterable

TEXT_EXTENSIONS = {
    "",
    ".bat",
    ".cfg",
    ".cmd",
    ".css",
    ".csv",
    ".env",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsonl",
    ".jsx",
    ".md",
    ".ps1",
    ".py",
    ".pyi",
    ".scss",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

GENERIC_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9.-])"),
    re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)"),
)


def normalize_git_path(path: str) -> str:
    return path.replace("\\", "/").removeprefix("./")


def find_violations(path: str, content: str, sensitive_terms: Iterable[str]) -> list[str]:
    normalized = normalize_git_path(path)
    violations: list[str] = []

    if normalized == "wiki" or normalized.startswith("wiki/"):
        return [f"禁止提交 wiki 路径：{normalized}"]

    lowered = content.casefold()
    if any(term.strip() and term.strip().casefold() in lowered for term in sensitive_terms):
        violations.append(f"在 {normalized} 中检测到本机敏感词")

    if any(pattern.search(content) for pattern in GENERIC_PATTERNS):
        violations.append(f"在 {normalized} 中检测到可能的联系方式或证件号码")

    return violations


def run_git(repository_root: Path, *args: str, binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=not binary,
    )
    return completed.stdout


def load_sensitive_terms(path: Path) -> list[str]:
    if not path.is_file():
        raise RuntimeError("缺少 .local/sensitive_terms.txt，拒绝提交。")
    terms = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not terms:
        raise RuntimeError("本机敏感词清单为空，拒绝提交。")
    return terms


def get_staged_paths(repository_root: Path) -> list[str]:
    output = run_git(
        repository_root,
        "diff",
        "--cached",
        "--name-only",
        "--diff-filter=ACMR",
        "-z",
        binary=True,
    )
    assert isinstance(output, bytes)
    return [item.decode("utf-8", errors="surrogateescape") for item in output.split(b"\0") if item]


def get_staged_text(repository_root: Path, path: str) -> str:
    output = run_git(repository_root, "show", f":{path}", binary=True)
    assert isinstance(output, bytes)
    return output.decode("utf-8", errors="replace")


def main() -> int:
    try:
        root_output = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        repository_root = Path(root_output)
        sensitive_terms = load_sensitive_terms(repository_root / ".local" / "sensitive_terms.txt")
        violations: list[str] = []

        for path in get_staged_paths(repository_root):
            normalized = normalize_git_path(path)
            if normalized == "wiki" or normalized.startswith("wiki/"):
                violations.extend(find_violations(path, "", sensitive_terms))
                continue
            if PurePosixPath(normalized).suffix.casefold() not in TEXT_EXTENSIONS:
                continue
            violations.extend(
                find_violations(path, get_staged_text(repository_root, path), sensitive_terms)
            )

        if violations:
            print("提交被仓库隐私策略阻止：", file=sys.stderr)
            for violation in sorted(set(violations)):
                print(f" - {violation}", file=sys.stderr)
            return 1

        print("跨平台敏感内容检查通过。")
        return 0
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
