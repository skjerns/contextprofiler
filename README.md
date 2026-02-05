# ContextProfiler

A simple line-by-line profiler for Python code blocks using context managers.

```bash
pip install contextprofiler
```

```python
import contextprofiler
import time

with contextprofiler:
    time.sleep(0.1)
    x = sum(range(10000))
    time.sleep(0.05)
```

Output:
```
--------------------------------------------------------------------------------
Line-by-Line Profile
--------------------------------------------------------------------------------
64.5% 000.100s | time.sleep(0.1)
 2.3% 000.004s | x = sum(range(10000))
33.2% 000.052s | time.sleep(0.05)
--------------------------------------------------------------------------------
Total time: 0.1560s
--------------------------------------------------------------------------------
```

You can also use `from contextprofiler import ContextProfiler` and `with ContextProfiler:`, or create independent instances with `ContextProfiler()` when you need isolation. The profiler exits cleanly on exceptions, printing results before propagating.

Uses `sys.settrace()` to trace line execution. Only profiles the immediate code block, not called functions. Colors range from white (low %) to red (high %) when supported.

## License

MIT License - see [LICENSE](LICENSE) for details.
