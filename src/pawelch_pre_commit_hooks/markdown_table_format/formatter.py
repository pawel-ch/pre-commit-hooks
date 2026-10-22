"""Pipe table formatting: column widths, alignment markers, and fenced-code awareness."""

from __future__ import annotations

import re
import unicodedata
from itertools import starmap

SEPARATOR_CELL = re.compile(r"^\s*:?-+:?\s*$")
FENCE = re.compile(r"\s*(```+|~~~+)")


def text_width(text: str) -> int:
    """Return the display width of text (wide and full-width characters count as two columns)."""
    total = 0
    for char in text:
        if unicodedata.combining(char):
            continue
        total += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
    return total


def split_row(line: str) -> list[str]:
    """Split a table row into stripped cells, keeping escaped pipes and pipes inside code spans."""
    body = line.strip().removeprefix("|")
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells: list[str] = []
    current = ""
    in_code = False
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body):
            current += body[index : index + 2]
            index += 2
            continue
        if char == "`":
            in_code = not in_code
        if char == "|" and not in_code:
            cells.append(current.strip())
            current = ""
        else:
            current += char
        index += 1
    cells.append(current.strip())
    return cells


def _alignment(separator_cell: str) -> str:
    cell = separator_cell.strip()
    left, right = cell.startswith(":"), cell.endswith(":")
    if left and right:
        return "center"
    if right:
        return "right"
    return "left" if left else ""


def _separator(width: int, alignment: str) -> str:
    dashes = "-" * (width + 2)
    if alignment in {"left", "center"}:
        dashes = ":" + dashes[1:]
    if alignment in {"right", "center"}:
        dashes = dashes[:-1] + ":"
    return dashes


def _pad(text: str, width: int, alignment: str) -> str:
    gap = width - text_width(text)
    if alignment == "right":
        return " " * gap + text
    if alignment == "center":
        return " " * (gap // 2) + text + " " * (gap - gap // 2)
    return text + " " * gap


def format_table(lines: list[str]) -> list[str]:
    """Format one table given as its lines (header, separator, body rows)."""
    indent = re.match(r"\s*", lines[0]).group(0)
    rows = [split_row(line) for line in lines]
    column_count = max(len(row) for row in rows)
    rows = [row + [""] * (column_count - len(row)) for row in rows]
    alignments = [_alignment(cell) for cell in rows[1]]
    content_rows = [row for number, row in enumerate(rows) if number != 1]
    widths = [max([text_width(row[column]) for row in content_rows] + [1]) for column in range(column_count)]
    formatted = []
    for number, row in enumerate(rows):
        if number == 1:
            cells = list(starmap(_separator, zip(widths, alignments, strict=True)))
        else:
            cells = [f" {_pad(text, width, alignment)} " for text, width, alignment in zip(row, widths, alignments, strict=True)]
        formatted.append(indent + "|" + "|".join(cells) + "|")
    return formatted


def _is_table_start(lines: list[str], index: int) -> bool:
    return (
        lines[index].lstrip().startswith("|")
        and index + 1 < len(lines)
        and lines[index + 1].lstrip().startswith("|")
        and all(SEPARATOR_CELL.match(cell) for cell in split_row(lines[index + 1]))
    )


def format_markdown(text: str) -> str:
    """Format every pipe table in a Markdown document, leaving fenced code blocks untouched."""
    lines = text.split("\n")
    result: list[str] = []
    fence: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if match := FENCE.match(line):
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
        elif fence is None and _is_table_start(lines, index):
            end = index + 2
            while end < len(lines) and lines[end].lstrip().startswith("|"):
                end += 1
            result.extend(format_table(lines[index:end]))
            index = end
            continue
        result.append(line)
        index += 1
    return "\n".join(result)
