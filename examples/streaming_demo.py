# -*- coding: utf-8 -*-
"""Low-latency streaming profile demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import load_config, DramaEngine


def main():
    cfg = load_config("configs/streaming.yaml")
    engine = DramaEngine(cfg)
    r = engine.synth("低延迟流式合成演示。")
    print("streaming config -> %.3fs audio, %d samples" % (r.duration_s, len(r.waveform)))


if __name__ == "__main__":
    main()
