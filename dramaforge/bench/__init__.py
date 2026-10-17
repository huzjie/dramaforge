"""Benchmarks: directive adherence, MOS, speaker similarity, switch, RVQ."""
from .registry import register_benchmark, BENCHMARKS, list_benchmarks
from . import directive_consistency, mos, similarity, speaker_switch, rvq  # noqa: F401
from .runner import run_all, summarize

__all__ = ["register_benchmark", "BENCHMARKS", "list_benchmarks", "run_all", "summarize"]
