"""
ContextProfiler - A simple line-by-line profiler for Python code blocks.

Usage:
    # Option 1: Import and use the module directly
    import contextprofiler
    with contextprofiler:
        # code to profile
        ...

    # Option 2: Import ContextProfiler explicitly
    from contextprofiler import ContextProfiler
    with ContextProfiler:
        # code to profile
        ...

    # Option 3: Create a fresh instance
    with ContextProfiler():
        # code to profile
        ...
"""

from __future__ import annotations

import sys
import types

if sys.version_info < (3, 10):
    raise RuntimeError("contextprofiler requires Python 3.10 or later")

from contextprofiler._profiler import _ProfilerImpl

__version__ = "0.1.0"
__all__ = ["ContextProfiler", "__version__"]

# Shared, callable instance for 'with ContextProfiler:' and 'with ContextProfiler():'
ContextProfiler = _ProfilerImpl()


class _ModuleWithContextManager(types.ModuleType):
    """Module wrapper that supports the context manager protocol."""

    def __enter__(self):
        return ContextProfiler.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return ContextProfiler.__exit__(exc_type, exc_val, exc_tb)


# Replace this module with our context-manager-enabled version
_new_module = _ModuleWithContextManager(__name__)
_new_module.__dict__.update(sys.modules[__name__].__dict__)
sys.modules[__name__] = _new_module
