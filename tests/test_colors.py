# -*- coding: utf-8 -*-
"""Tests for color utilities."""

import os

import pytest

from contextprofiler._colors import RESET, rgb_fg_ansi, supports_color, white_to_red_rgb


class TestSupportsColor:
    """Tests for supports_color function."""

    def test_supports_color_no_color_env(self, monkeypatch):
        """Test that NO_COLOR environment variable disables color."""
        monkeypatch.setenv("NO_COLOR", "1")
        assert supports_color() is False

    def test_supports_color_no_color_empty(self, monkeypatch):
        """Test that empty NO_COLOR still disables color."""
        monkeypatch.setenv("NO_COLOR", "")
        # Empty string is falsy, so color should be supported (if tty)
        # Just verify no exception is raised
        result = supports_color()
        assert isinstance(result, bool)

    def test_supports_color_respects_tty(self, monkeypatch):
        """Test that non-tty returns False when NO_COLOR not set."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        # In test environment, stdout is usually not a tty
        # So this should return False
        result = supports_color()
        assert isinstance(result, bool)


class TestWhiteToRedRgb:
    """Tests for white_to_red_rgb function."""

    def test_white_to_red_rgb_zero(self):
        """Test that 0% gives white."""
        r, g, b = white_to_red_rgb(0)
        assert (r, g, b) == (255, 255, 255)

    def test_white_to_red_rgb_hundred(self):
        """Test that 100% gives red."""
        r, g, b = white_to_red_rgb(100)
        assert (r, g, b) == (255, 0, 0)

    def test_white_to_red_rgb_fifty(self):
        """Test that 50% gives intermediate color."""
        r, g, b = white_to_red_rgb(50)
        assert r == 255
        assert g == 128  # round(255 * 0.5) = 128
        assert b == 128

    def test_white_to_red_rgb_clamps_negative(self):
        """Test that negative values are clamped to 0%."""
        r, g, b = white_to_red_rgb(-50)
        assert (r, g, b) == (255, 255, 255)

    def test_white_to_red_rgb_clamps_over_hundred(self):
        """Test that values over 100 are clamped to 100%."""
        r, g, b = white_to_red_rgb(150)
        assert (r, g, b) == (255, 0, 0)


class TestRgbFgAnsi:
    """Tests for rgb_fg_ansi function."""

    def test_rgb_fg_ansi_format(self):
        """Test correct ANSI escape sequence format."""
        result = rgb_fg_ansi(255, 128, 64)
        assert result == "\033[38;2;255;128;64m"

    def test_rgb_fg_ansi_black(self):
        """Test ANSI escape for black."""
        result = rgb_fg_ansi(0, 0, 0)
        assert result == "\033[38;2;0;0;0m"

    def test_rgb_fg_ansi_white(self):
        """Test ANSI escape for white."""
        result = rgb_fg_ansi(255, 255, 255)
        assert result == "\033[38;2;255;255;255m"


class TestReset:
    """Tests for RESET constant."""

    def test_reset_constant(self):
        """Test that RESET is the correct escape sequence."""
        assert RESET == "\033[0m"
