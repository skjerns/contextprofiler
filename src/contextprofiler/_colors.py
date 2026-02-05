"""Color utilities for terminal output."""

from __future__ import annotations

import os
import sys

RESET = "\033[0m"


def supports_color() -> bool:
    """Returns True if ANSI color is likely supported."""
    if os.environ.get("NO_COLOR"):
        return False
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def white_to_red_rgb(pct: float) -> tuple[int, int, int]:
    """Maps 0-100 pct to RGB from white to red."""
    t = max(0.0, min(1.0, pct / 100.0))
    r = 255
    g = int(round(255 * (1.0 - t)))
    b = int(round(255 * (1.0 - t)))
    return r, g, b


def rgb_fg_ansi(r: int, g: int, b: int) -> str:
    """Returns ANSI escape for 24-bit RGB foreground."""
    return f"\033[38;2;{r};{g};{b}m"
