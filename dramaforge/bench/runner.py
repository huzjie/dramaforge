"""Benchmark runner + summary."""
from .registry import BENCHMARKS


def run_all(engine, names=None):
    results = {}
    for name, fn in BENCHMARKS.items():
        if names is not None and name not in names:
            continue
        try:
            results[name] = fn(engine)
        except Exception as e:  # pragma: no cover
            results[name] = {"error": str(e)}
    return results


def summarize(results):
    lines = []
    for k, v in results.items():
        if "error" in v:
            lines.append("  %-22s ERROR %s" % (k, v["error"]))
        else:
            lines.append("  %-22s %s" % (k, v))
    return "\n".join(lines)
