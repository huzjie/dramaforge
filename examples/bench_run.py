# -*- coding: utf-8 -*-
"""Run all benchmarks."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config, DramaEngine
from dramaforge.bench import run_all, summarize


def main():
    engine = DramaEngine(Config())
    print(summarize(run_all(engine)))


if __name__ == "__main__":
    main()
