# -*- coding: utf-8 -*-
"""Train the mock backend's directive-obedience skill 0.5 -> 1.0."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dramaforge import Config
from dramaforge.backends import get_backend
from dramaforge.train import Trainer


def main():
    cfg = Config()
    backend = get_backend("mock", cfg)
    trainer = Trainer(backend)
    print("skill before: %.4f" % backend.skill)
    for step, (b, a) in enumerate(trainer.train(20), 1):
        if step % 5 == 0:
            print("  step %2d: %.4f -> %.4f" % (step, b, a))
    print("skill after:  %.4f" % backend.skill)


if __name__ == "__main__":
    main()
