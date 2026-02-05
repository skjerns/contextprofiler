# -*- coding: utf-8 -*-
"""Integration tests for contextprofiler."""

import subprocess
import sys


class TestRealComputation:
    """Tests with real CPU work."""

    def test_real_computation(self, capsys, no_color_env):
        """Test profiling actual CPU work."""
        from contextprofiler import ContextProfiler

        with ContextProfiler:
            total = 0
            for i in range(1000):
                total += i * i

        captured = capsys.readouterr()
        assert "Line-by-Line Profile" in captured.out
        assert "Total time:" in captured.out

    def test_nested_function_calls(self, capsys, no_color_env):
        """Test profiling with nested function calls."""
        from contextprofiler import ContextProfiler

        def helper(n):
            return sum(range(n))

        with ContextProfiler:
            result = helper(100)
            result += helper(200)

        captured = capsys.readouterr()
        assert "helper(100)" in captured.out
        assert "helper(200)" in captured.out


class TestSubprocessRun:
    """Tests running profiler in a subprocess."""

    def test_subprocess_run(self):
        """Verify console output format in a real subprocess."""
        code = '''
import time
from contextprofiler import ContextProfiler

with ContextProfiler:
    time.sleep(0.01)
    x = 1 + 1
'''
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "NO_COLOR": "1"},
        )

        assert result.returncode == 0
        assert "Line-by-Line Profile" in result.stdout
        assert "Total time:" in result.stdout
        # Note: linecache may not find source for -c code, so lines may be empty

    def test_subprocess_exception(self):
        """Test that exceptions propagate correctly in subprocess."""
        code = '''
from contextprofiler import ContextProfiler

try:
    with ContextProfiler:
        x = 1
        raise ValueError("test")
except ValueError:
    print("CAUGHT")
'''
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "NO_COLOR": "1"},
        )

        assert result.returncode == 0
        assert "CAUGHT" in result.stdout
        assert "Line-by-Line Profile" in result.stdout
