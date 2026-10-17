"""Trainer for the mock backend's directive-obedience skill.

The skill starts at 0.5 (random adherence) and climbs monotonically toward 1.0
(perfect adherence). The update is deliberately always positive: ``delta =
lr * (1 - skill)``, so the curve is clean and reproducible -- the point is to
demonstrate that "train to obey directives better" is a well-posed signal, not
to actually fit a neural network.
"""


class Trainer:
    def __init__(self, backend, lr=0.5):
        self.backend = backend
        self.lr = lr

    def step(self):
        """One training step: skill moves monotonically toward 1.0."""
        before = self.backend.skill
        self.backend.skill = min(1.0, before + self.lr * (1.0 - before))
        return before, self.backend.skill

    def train(self, steps=20):
        hist = []
        for _ in range(steps):
            before, after = self.step()
            hist.append((round(before, 4), round(after, 4)))
        return hist
