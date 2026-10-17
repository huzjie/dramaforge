# -*- coding: utf-8 -*-
"""Example: run with `python examples/directable_synth.py` from the project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config, DramaEngine


def main():
    cfg = Config()
    engine = DramaEngine(cfg)

    text = "[emotion=angry]我真的受够了！[/emotion] 然后她[rate=0.8]慢慢地说[/rate]，" \
           "[emotion=gentle]没关系，我们慢慢来。[/emotion]"
    r = engine.synth(text)
    print(r.as_dict())
    print("word attrs:")
    for a in r.word_attrs:
        print("  %-8s emotion=%-9s rate=%.2f" % (a.text, a.emotion, a.rate))


if __name__ == "__main__":
    main()
