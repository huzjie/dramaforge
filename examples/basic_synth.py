# -*- coding: utf-8 -*-
"""Example: run with `python examples/basic_synth.py` from the project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config, DramaEngine


def main():
    cfg = Config()
    engine = DramaEngine(cfg)

    r = engine.synth("你好，欢迎使用 dramaforge 可执导语音合成引擎。")
    print(r.as_dict())
    from dramaforge.engine.audio import save_wav
    save_wav("basic.wav", r.waveform, r.sample_rate)
    print("saved basic.wav")


if __name__ == "__main__":
    main()
