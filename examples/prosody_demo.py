# -*- coding: utf-8 -*-
"""Prosody prediction demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge.directive import Directive, apply_directives
from dramaforge.utils.text import tokenize_words
from dramaforge.prosody import ProsodyPredictor


def main():
    words = tokenize_words("这句话说得很平静，但是这一句很激动")
    attrs = apply_directives(words, [Directive(0, len(words), emotion="excited")])
    p = ProsodyPredictor(frame_rate=50, pitch_bins=12)
    pitch, energy, dur = p.predict(attrs)
    print("frames=%d, avg_pitch=%.3f, avg_energy=%.3f" %
          (len(pitch), sum(pitch) / len(pitch), sum(energy) / len(energy)))


if __name__ == "__main__":
    main()
