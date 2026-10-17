# -*- coding: utf-8 -*-
"""Example: run with `python examples/multi_speaker.py` from the project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config, DramaEngine


def main():
    cfg = Config()
    engine = DramaEngine(cfg)

    dialogue = ("[voice=alice]你好，请问是技术支持吗？[/voice] "
                "[voice=bob]是的，请问有什么可以帮您？[/voice] "
                "[voice=alice]我的账号登录不上了。[/voice]")
    r = engine.synth(dialogue)
    print(r.as_dict())
    print("speaker turns:")
    for t in r.turns:
        print("  %-8s words %d..%d" % (t.speaker, t.start_word, t.end_word))


if __name__ == "__main__":
    main()
