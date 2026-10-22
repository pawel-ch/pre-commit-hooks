import pytest

from pawelch_pre_commit_hooks.markdown_table_format import format_markdown
from pawelch_pre_commit_hooks.markdown_table_format import split_row
from pawelch_pre_commit_hooks.markdown_table_format import text_width

UNFORMATTED = """\
| Title | Director | Year | Watched |
|---|---|---|---|
| 2001: A Space Odyssey | Stanley Kubrick | 1968 | yes |
| Spirited Away | Hayao Miyazaki | 2001 | no |
"""

FORMATTED = """\
| Title                 | Director        | Year | Watched |
|-----------------------|-----------------|------|---------|
| 2001: A Space Odyssey | Stanley Kubrick | 1968 | yes     |
| Spirited Away         | Hayao Miyazaki  | 2001 | no      |
"""


def test_formats_table_pycharm_style():
    assert format_markdown(UNFORMATTED) == FORMATTED


def test_is_idempotent():
    assert format_markdown(FORMATTED) == FORMATTED


def test_preserves_alignment_markers():
    text = """\
| Title | Year | Status |
|:--|--:|:-:|
| Metropolis | 1927 | seen |
"""
    expected = """\
| Title      | Year | Status |
|:-----------|-----:|:------:|
| Metropolis | 1927 |  seen  |
"""
    assert format_markdown(text) == expected


def test_right_and_center_alignment_pad_content():
    text = """\
| Minutes | Rating |
|--:|:-:|
| 96 | PG |
| 201 | PG-13 |
"""
    expected = """\
| Minutes | Rating |
|--------:|:------:|
|      96 |   PG   |
|     201 | PG-13  |
"""
    assert format_markdown(text) == expected


def test_leaves_fenced_code_untouched():
    text = """\
```
| Title | Year |
|---|---|
| Alien | 1979 |
```
"""
    assert format_markdown(text) == text


def test_ignores_pipe_lines_without_separator_row():
    text = """\
| Casablanca |
| The Third Man |
"""
    assert format_markdown(text) == text


def test_keeps_indentation_of_tables_in_lists():
    text = """\
- Watchlist

  | Title | Year |
  |---|---|
  | Jaws | 1975 |
  | Chinatown | 1974 |
"""
    expected = """\
- Watchlist

  | Title     | Year |
  |-----------|------|
  | Jaws      | 1975 |
  | Chinatown | 1974 |
"""
    assert format_markdown(text) == expected


def test_pads_missing_cells():
    text = """\
| Title | Director |
|---|---|
| Nosferatu |
"""
    expected = """\
| Title     | Director |
|-----------|----------|
| Nosferatu |          |
"""
    assert format_markdown(text) == expected


@pytest.mark.parametrize(
    ("line", "cells"),
    [
        ("| Heat | 1995 |", ["Heat", "1995"]),
        ("| `Face|Off` | 1997 |", ["`Face|Off`", "1997"]),
        (r"| Kill Bill \| Vol. 1 | 2003 |", [r"Kill Bill \| Vol. 1", "2003"]),
        ("Heat | 1995", ["Heat", "1995"]),
    ],
)
def test_split_row(line, cells):
    assert split_row(line) == cells


@pytest.mark.parametrize(("text", "width"), [("Heat", 4), ("Amélie", 6), ("✅", 2), ("千と千尋", 8), ("Ame\u0301lie", 6)])
def test_text_width(text, width):
    assert text_width(text) == width
