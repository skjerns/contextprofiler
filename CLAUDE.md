# ContextProfiler Development Notes

## Project Overview
A line-by-line profiler for Python code blocks using context managers. Uses `sys.settrace()` to trace execution.

## Structure
```
contextprofiler/
├── contextprofiler/      # Package (flat layout, no src/)
│   ├── __init__.py       # Exports: ContextProfiler, __version__
│   ├── _profiler.py      # Core _ProfilerImpl class
│   ├── _colors.py        # ANSI color utilities
│   └── py.typed          # PEP 561 marker
├── tests/                # pytest tests (25 total)
└── pyproject.toml        # hatchling build
```

## Development Commands
```bash
pip install -e ".[dev]"   # Install with dev deps
pytest -v                 # Run tests
mypy contextprofiler/     # Type check
ruff check contextprofiler/  # Lint
python -m build           # Build wheel/sdist
```

## Key Design Decisions
- **Singleton pattern**: `ContextProfiler` is a pre-instantiated `_ProfilerImpl()` that's also callable to create fresh instances
- **No dependencies**: stdlib only (inspect, linecache, sys, time, collections)
- **Color support**: Respects `NO_COLOR` env var, auto-detects TTY
- **Python 3.8+**: Uses `from __future__ import annotations` for modern type hints

## Testing Notes
- Use `no_color_env` fixture when checking output format
- Subprocess tests can't verify line content (linecache doesn't work with `-c` code)
- `pass` statement counts as a profiled line (not "empty block")

## CI/CD
- `.github/workflows/test.yml`: Tests on Python 3.8-3.13
- `.github/workflows/publish.yml`: PyPI trusted publishing on release
