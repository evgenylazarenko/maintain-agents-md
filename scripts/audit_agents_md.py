#!/usr/bin/env python3
"""Audit nested AGENTS.md files for sprawl and promotion issues."""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    "deps",
    "node_modules",
    ".next",
    "dist",
    "build",
    ".venv",
    "vendor",
}

STALE_WORDING = (
    "AGENTS.md Draft For",
    "Proposed Nested Scope",
    "proposed nested scope",
    "Install separate copies",
)

LIVING = "Living doc: every pass MUST review/tweak this file as guidance emerges/expires."
STYLE = "Style guard: keep this file short, scoped, and deduplicated;"


def iter_agents(repo: Path, excludes: set[str]) -> list[Path]:
    results: list[Path] = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in excludes]
        if "AGENTS.md" in files:
            results.append(Path(root) / "AGENTS.md")
    return sorted(results)


def rel(repo: Path, path: Path) -> str:
    return str(path.relative_to(repo))


def git_check_ignore(repo: Path, files: list[Path]) -> list[tuple[str, str]]:
    if not files:
        return []
    cmd = ["git", "check-ignore", "-v", *[rel(repo, f) for f in files]]
    proc = subprocess.run(cmd, cwd=repo, text=True, capture_output=True, check=False)
    if proc.returncode not in (0, 1):
        return [("git check-ignore failed", proc.stderr.strip())]
    ignored = []
    for line in proc.stdout.splitlines():
        parts = line.split("\t", 1)
        if len(parts) == 2:
            ignored.append((parts[1], parts[0]))
    return ignored


def load_gitignore_patterns(repo: Path) -> list[str]:
    path = repo / ".gitignore"
    if not path.exists():
        return []
    patterns = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def likely_ignored_by_pattern(path: str, patterns: list[str]) -> bool:
    name = Path(path).name
    for pattern in patterns:
        normalized = pattern.rstrip("/")
        if normalized == name or fnmatch.fnmatch(path, normalized) or fnmatch.fnmatch(name, normalized):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit nested AGENTS.md files.")
    parser.add_argument("repo", type=Path, help="Repository root")
    parser.add_argument("--max-lines", type=int, default=80, help="Warn when a local AGENTS.md exceeds this line count")
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory name to exclude")
    parser.add_argument("--allow-ignored", action="store_true", help="Report ignored AGENTS.md files without failing")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not (repo / ".git").exists():
        print(f"ERROR: {repo} does not look like a git repository", file=sys.stderr)
        return 2

    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    files = iter_agents(repo, excludes)
    root = repo / "AGENTS.md"
    local_files = [p for p in files if p != root]
    patterns = load_gitignore_patterns(repo)

    warnings: list[str] = []
    print(f"AGENTS.md files: {len(files)}")
    for path in files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        path_rel = rel(repo, path)
        print(f"- {path_rel}: {len(lines)} lines")

        if path != root and len(lines) > args.max_lines:
            warnings.append(f"{path_rel}: exceeds --max-lines={args.max_lines} ({len(lines)} lines)")
        if any(marker in text for marker in STALE_WORDING):
            warnings.append(f"{path_rel}: contains draft/proposed wording")
        if path != root and LIVING not in text:
            warnings.append(f"{path_rel}: missing living-doc guard")
        if path != root and STYLE not in text:
            warnings.append(f"{path_rel}: missing style guard")
        for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if line.rstrip() != line:
                warnings.append(f"{path_rel}:{idx}: trailing whitespace")

    ignored = git_check_ignore(repo, files)
    for path_rel, source in ignored:
        message = f"{path_rel}: ignored by {source}"
        if args.allow_ignored:
            print(f"NOTE: {message}")
        else:
            warnings.append(message)

    if not ignored:
        for path in files:
            path_rel = rel(repo, path)
            if likely_ignored_by_pattern(path_rel, patterns):
                message = f"{path_rel}: likely ignored by .gitignore pattern"
                if args.allow_ignored:
                    print(f"NOTE: {message}")
                else:
                    warnings.append(message)

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("\nNo warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
