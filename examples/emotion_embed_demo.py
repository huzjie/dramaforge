# -*- coding: utf-8 -*-
"""Emotion embedding demo."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge.emotion import EmotionEmbedder
from dramaforge.utils.vectors import cosine


def main():
    emb = EmotionEmbedder(embed_dim=16, n_emotions=8)
    pairs = [("angry", "happy"), ("angry", "sad"), ("angry", "neutral"), ("happy", "sad")]
    for a, b in pairs:
        print("%-8s ~ %-8s cosine=%.3f" % (a, b, cosine(emb.embed(a), emb.embed(b))))


if __name__ == "__main__":
    main()
