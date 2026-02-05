"""Core profiler implementation."""

from __future__ import annotations

import inspect
import linecache
import sys
import time
from collections import defaultdict
from types import FrameType, TracebackType
from typing import Any

from ._colors import RESET, rgb_fg_ansi, supports_color, white_to_red_rgb


class _ProfilerImpl:
    """
    Line profiler for Python code blocks.

    Traces a single frame entered via context manager and reports line timings.
    Can be used as a singleton or instantiated for independent profiling sessions.
    """

    def __init__(self) -> None:
        self._reset()
        self._use_color = supports_color()

    def _reset(self) -> None:
        """Resets the profiler's state to allow for multiple runs."""
        self._timings: defaultdict[int, float] = defaultdict(float)
        self._lines: dict[int, str] = {}
        self._start_time: float = 0
        self._last_time: float = 0
        self._target_frame: FrameType | None = None
        self._entry_lineno: int = -1
        self._last_lineno: int = -1

    def __enter__(self) -> _ProfilerImpl:
        """Starts the profiling, gets the target frame, and sets the trace."""
        self._reset()
        frame = inspect.currentframe()
        assert frame is not None
        # Walk up until we find a frame outside this module file
        this_file = frame.f_code.co_filename
        pkg_dir = this_file.rsplit("/", 1)[0] if "/" in this_file else ""
        while frame is not None:
            frame = frame.f_back
            if frame is None:
                break
            filename = frame.f_code.co_filename
            # Stop when we exit the contextprofiler package directory
            if not filename.startswith(pkg_dir):
                break
        assert frame is not None, "Could not find caller frame"
        self._target_frame = frame
        self._entry_lineno = self._target_frame.f_lineno
        self._start_time = time.perf_counter()
        self._last_time = self._start_time
        self._last_lineno = self._entry_lineno
        self._target_frame.f_trace = self._trace_function
        sys.settrace(self._trace_function)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Stops profiling, finalizes timing, and prints results."""
        sys.settrace(None)
        if self._target_frame:
            self._target_frame.f_trace = None
        final_time = time.perf_counter()
        self._record_timing(self._last_lineno, final_time)
        self._print_results()
        self._target_frame = None

    def _trace_function(self, frame: FrameType, event: str, arg: Any) -> Any:
        """Tracing callback for each executed line in the target frame."""
        if event == "line" and frame is self._target_frame:
            current_time = time.perf_counter()
            self._record_timing(self._last_lineno, current_time)
            self._last_time = current_time
            self._last_lineno = frame.f_lineno
        return self._trace_function

    def _record_timing(self, lineno: int, end_time: float) -> None:
        """Stores execution time for a line, ignoring the 'with' line."""
        if lineno == self._entry_lineno:
            return
        elapsed = end_time - self._last_time
        self._timings[lineno] += elapsed
        if lineno not in self._lines and self._target_frame is not None:
            filename = self._target_frame.f_code.co_filename
            self._lines[lineno] = linecache.getline(filename, lineno).rstrip("\n")

    def _fmt_line(self, percentage: float, line_time: float, line_text: str) -> str:
        """Formats a single output line with optional color."""
        pct_str = f"{percentage:04.1f}%"
        time_str = f"{line_time:07.3f}s"
        line_text = line_text.replace("  ", " ")
        base = f"{pct_str} {time_str} | {line_text.rstrip()}"
        if not self._use_color:
            return base
        r, g, b = white_to_red_rgb(percentage)
        return f"{rgb_fg_ansi(r, g, b)}{base}{RESET}"

    def _print_results(self) -> None:
        """Prints results sorted by descending percentage with color mapping."""
        if not self._timings:
            print("No lines were profiled in the block.")
            return

        total_time = sum(self._timings.values())
        rows = []
        for lineno, line_time in self._timings.items():
            pct = (line_time / total_time) * 100 if total_time > 0 else 0.0
            rows.append((pct, line_time, self._lines.get(lineno, "")))

        print("-" * 80)
        print("Line-by-Line Profile")
        print("-" * 80)
        for pct, line_time, text in rows:
            print(self._fmt_line(pct, line_time, text))
        print("-" * 80)
        print(f"Total time: {total_time:.4f}s")
        print("-" * 80)

    def __call__(self) -> _ProfilerImpl:
        """Returns a fresh independent profiler instance."""
        return _ProfilerImpl()
