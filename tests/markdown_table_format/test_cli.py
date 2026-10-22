from pawelch_pre_commit_hooks.markdown_table_format.cli import main

UNFORMATTED = """\
| Title | Year |
|---|---|
| Vertigo | 1958 |
"""

FORMATTED = """\
| Title   | Year |
|---------|------|
| Vertigo | 1958 |
"""


def test_rewrites_file_and_reports_change(tmp_path, capsys):
    path = tmp_path / "watchlist.md"
    path.write_text(UNFORMATTED, encoding="utf-8")
    assert main([str(path)]) == 1
    assert path.read_text(encoding="utf-8") == FORMATTED
    assert "Reformatted" in capsys.readouterr().err


def test_returns_zero_for_formatted_file(tmp_path):
    path = tmp_path / "watchlist.md"
    path.write_text(FORMATTED, encoding="utf-8")
    assert main([str(path)]) == 0


def test_check_mode_does_not_modify(tmp_path):
    path = tmp_path / "watchlist.md"
    path.write_text(UNFORMATTED, encoding="utf-8")
    assert main(["--check", str(path)]) == 1
    assert path.read_text(encoding="utf-8") == UNFORMATTED
