"""
ContextProfiler - A simple line-by-line profiler for Python code blocks.

Usage:
    from contextprofiler import ContextProfiler

    with ContextProfiler:
        # code to profile
        ...

    # Or create a fresh instance:
    with ContextProfiler():
        # code to profile
        ...
"""

from contextprofiler._profiler import _ProfilerImpl

__version__ = "0.1.0"
__all__ = ["ContextProfiler", "__version__"]

# Shared, callable instance for 'with ContextProfiler:' and 'with ContextProfiler():'
ContextProfiler = _ProfilerImpl()
