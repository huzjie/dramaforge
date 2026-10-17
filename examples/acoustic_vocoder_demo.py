# -*- coding: utf-8 -*-
"""Two-stage acoustic -> vocoder waveform demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config, DramaEngine
from dramaforge.engine.audio import save_wav


def main():
    engine = DramaEngine(Config())
    r = engine.synth("两阶段声学到声码的波形演示。")
    save_wav("two_stage.wav", r.waveform, r.sample_rate)
    print("duration=%.3fs samples=%d" % (r.duration_s, len(r.waveform)))
    print("saved two_stage.wav")


if __name__ == "__main__":
    main()
