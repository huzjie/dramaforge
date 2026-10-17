# -*- coding: utf-8 -*-
"""Speaker library + separation demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge.speaker import SpeakerLibrary, speaker_similarity


def main():
    lib = SpeakerLibrary(n_speakers=8, embed_dim=32, seed=7)
    names = lib.list_speakers()
    print("speakers:", names)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            s = speaker_similarity(lib.get(a).embedding, lib.get(b).embedding)
            if s > 0.3:
                print("  close pair: %s~%s sim=%.3f" % (a, b, s))
    print("self similarity:", speaker_similarity(lib.get("alice").embedding, lib.get("alice").embedding))


if __name__ == "__main__":
    main()
