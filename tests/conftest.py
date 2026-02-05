# -*- coding: utf-8 -*-
"""pytest fixtures for contextprofiler tests."""

import os

import pytest


@pytest.fixture
def no_color_env(monkeypatch):
    """Set NO_COLOR environment variable to disable colors."""
    monkeypatch.setenv("NO_COLOR", "1")


@pytest.fixture
def force_color_env(monkeypatch):
    """Remove NO_COLOR to allow colors (if terminal supports it)."""
    monkeypatch.delenv("NO_COLOR", raising=False)
