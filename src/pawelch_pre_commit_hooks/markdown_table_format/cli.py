"""Command-line entry point compatible with pre-commit and prek hooks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pawelch_pre_commit_hooks.markdown_table_format import format_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="markdown-table-format", description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--check", action="store_true", help="report files that would change without modifying them")
    args = parser.parse_args(argv)

    changed = []
    for path in args.files:
        original = path.read_text(encoding="utf-8")
        formatted = format_markdown(original)
        if formatted != original:
            changed.append(path)
            if not args.check:
                path.write_text(formatted, encoding="utf-8")
    verb = "Would reformat" if args.check else "Reformatted"
    for path in changed:
        sys.stderr.write(f"{verb} {path}\n")
    return 1 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
