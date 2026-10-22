# pre-commit-hooks

Git hooks for [pre-commit](https://pre-commit.com) and [prek](https://prek.j178.dev).

| Hook id                 | Description                                       |
|-------------------------|---------------------------------------------------|
| `markdown-table-format` | Align Markdown table columns the way PyCharm does |

Supported Python versions: 3.11–3.15.

## Usage

prek (`prek.toml`):

```toml
[[repos]]
repo = "https://github.com/pawel-ch/pre-commit-hooks"
rev = "v0.1.0"
hooks = [{ id = "markdown-table-format" }]
```

pre-commit (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/pawel-ch/pre-commit-hooks
    rev: v0.1.0
    hooks:
      - id: markdown-table-format
```

## markdown-table-format

Aligns GFM pipe tables: every column is as wide as its longest cell, padded with one space on
each side, and the separator row is filled with dashes.

```markdown
| Title                 | Director        | Year | Watched |
|-----------------------|-----------------|------|---------|
| 2001: A Space Odyssey | Stanley Kubrick | 1968 | yes     |
| Spirited Away         | Hayao Miyazaki  | 2001 | no      |
```

Only tables change; the rest of the document is left as is. Tables inside fenced code blocks are
skipped, alignment markers (`:--`, `--:`, `:-:`) are kept, and wide characters (emoji, CJK) count
as two columns.

The hook rewrites files in place and exits with status 1 when anything changed, like other
formatting hooks. Run `markdown-table-format --check FILE...` to only report files that would change.

## Development

```bash
uv sync
uv run pytest
uv run prek run --all-files
```

## License

[MIT](LICENSE)
