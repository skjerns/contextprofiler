# -*- coding: utf-8 -*-
"""Tests for the core profiler functionality."""

import time

import pytest

from contextprofiler import ContextProfiler
from contextprofiler._profiler import _ProfilerImpl


class TestBasicProfiling:
    """Tests for basic profiling functionality."""

    def test_basic_profiling(self, capsys, no_color_env):
        """Test that profiling works and produces output."""
        with ContextProfiler:
            time.sleep(0.01)

        captured = capsys.readouterr()
        assert "Line-by-Line Profile" in captured.out
        assert "Total time:" in captured.out
        assert "time.sleep" in captured.out

    def test_multiple_lines(self, capsys, no_color_env):
        """Test that all lines appear in output."""
        with ContextProfiler:
            x = 1
            y = 2
            z = x + y

        captured = capsys.readouterr()
        assert "x = 1" in captured.out
        assert "y = 2" in captured.out
        assert "z = x + y" in captured.out

    def test_reusable_instance(self, capsys, no_color_env):
        """Test that the same instance can be used multiple times."""
        with ContextProfiler:
            x = 1

        with ContextProfiler:
            y = 2

        captured = capsys.readouterr()
        assert captured.out.count("Line-by-Line Profile") == 2

    def test_fresh_instance_call(self, capsys, no_color_env):
        """Test that ContextProfiler() returns a new instance."""
        profiler1 = ContextProfiler()
        profiler2 = ContextProfiler()

        assert profiler1 is not profiler2
        assert isinstance(profiler1, _ProfilerImpl)
        assert isinstance(profiler2, _ProfilerImpl)

    def test_module_as_context_manager(self, capsys, no_color_env):
        """Test that the module itself can be used as a context manager."""
        import contextprofiler

        with contextprofiler:
            time.sleep(0.01)

        captured = capsys.readouterr()
        assert "Line-by-Line Profile" in captured.out
        assert "time.sleep" in captured.out

    def test_exception_handling(self, capsys, no_color_env):
        """Test that profiler exits cleanly on exception."""
        with pytest.raises(ValueError):
            with ContextProfiler:
                x = 1
                raise ValueError("test error")

        captured = capsys.readouterr()
        # Should still print results before the exception propagates
        assert "Line-by-Line Profile" in captured.out
        assert "x = 1" in captured.out

    def test_empty_block(self, capsys, no_color_env):
        """Test handling of a block with only pass."""
        with ContextProfiler:
            pass

        captured = capsys.readouterr()
        # 'pass' is still a line that gets profiled
        assert "Line-by-Line Profile" in captured.out
        assert "pass" in captured.out


class TestTimingAccuracy:
    """Tests for timing accuracy."""

    def test_timing_accuracy(self, capsys, no_color_env):
        """Test that timing is approximately correct."""
        with ContextProfiler:
            time.sleep(0.05)

        captured = capsys.readouterr()
        # Extract total time from output
        for line in captured.out.split("\n"):
            if "Total time:" in line:
                # Format: "Total time: 0.0500s"
                time_str = line.split(":")[1].strip().rstrip("s")
                total_time = float(time_str)
                # Allow 20ms tolerance
                assert 0.03 < total_time < 0.15, f"Expected ~0.05s, got {total_time}s"
                break
        else:
            pytest.fail("Could not find 'Total time:' in output")


class TestOutputFormat:
    """Tests for output format."""

    def test_output_format(self, capsys, no_color_env):
        """Test that output contains expected elements."""
        with ContextProfiler:
            x = 1

        captured = capsys.readouterr()
        lines = captured.out.split("\n")

        # Check for header lines
        assert any("-" * 80 in line for line in lines)
        assert any("Line-by-Line Profile" in line for line in lines)

        # Check for percentage and time format in profiled lines
        for line in lines:
            if "x = 1" in line:
                # Format: "XX.X% XXX.XXXs | code"
                assert "%" in line
                assert "s" in line
                assert "|" in line
                break
        else:
            pytest.fail("Could not find profiled line in output")

    def test_percentage_calculation(self, capsys, no_color_env):
        """Test that percentages sum to approximately 100%."""
        with ContextProfiler:
            time.sleep(0.01)
            time.sleep(0.02)

        captured = capsys.readouterr()
        total_pct = 0.0
        for line in captured.out.split("\n"):
            if "%" in line and "|" in line:
                # Extract percentage
                pct_str = line.split("%")[0].strip()
                total_pct += float(pct_str)

        # Should sum to ~100%
        assert 99.0 < total_pct < 101.0, f"Percentages sum to {total_pct}%"
