# -*- coding: utf-8 -*-
"""Audio analysis demo (pitch / energy / zero-crossing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config, DramaEngine
from dramaforge.utils.audio_analysis import rms, zero_crossing_rate, autocorr_pitch


def main():
    engine = DramaEngine(Config())
    r = engine.synth("基频分析演示")
    print("rms=%.4f  zcr=%.4f  pitch=%.1f Hz" %
          (rms(r.waveform), zero_crossing_rate(r.waveform),
           autocorr_pitch(r.waveform, r.sample_rate) or 0.0))


if __name__ == "__main__":
    main()
