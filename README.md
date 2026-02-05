# ContextProfiler

A simple line-by-line profiler for Python code blocks using context managers.

## Installation

```bash
pip install contextprofiler
```

## Quick Start

```python
from contextprofiler import ContextProfiler
import time

with ContextProfiler:
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

## Usage

### Singleton Instance

Use the shared `ContextProfiler` instance for quick profiling:

```python
from contextprofiler import ContextProfiler

with ContextProfiler:
    # code to profile
    ...
```

### Fresh Instance

Create independent instances when you need isolation:

```python
from contextprofiler import ContextProfiler

with ContextProfiler():
    # profiled independently
    ...
```

### Exception Handling

The profiler exits cleanly on exceptions, printing results before the exception propagates:

```python
with ContextProfiler:
    x = expensive_operation()
    raise ValueError("oops")  # Results still printed
```

## How It Works

ContextProfiler uses Python's `sys.settrace()` mechanism to trace line execution within the profiled block. For each line executed:

1. Records the time since the previous line completed
2. Accumulates timing for lines executed multiple times (loops)
3. On exit, calculates percentages and prints a color-coded report

## Output

- **Percentage**: Time spent on this line relative to total block time
- **Time**: Absolute time in seconds
- **Code**: The source code of the line

Lines are displayed in execution order. Colors range from white (low percentage) to red (high percentage) when terminal colors are supported.

## Limitations

- Only profiles the immediate code block, not called functions
- Uses `sys.settrace()` which adds overhead (not for production use)
- Timing resolution depends on the system's `time.perf_counter()`

## License

MIT License - see [LICENSE](LICENSE) for details.
