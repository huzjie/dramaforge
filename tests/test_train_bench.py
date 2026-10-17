"""Trainer monotonicity + benchmark run."""
import unittest

from dramaforge import Config, DramaEngine
from dramaforge.backends import get_backend
from dramaforge.train import Trainer
from dramaforge.bench import run_all, list_benchmarks


class TestTrain(unittest.TestCase):
    def test_monotonic(self):
        cfg = Config()
        backend = get_backend("mock", cfg)
        t = Trainer(backend)
        hist = t.train(20)
        self.assertTrue(all(b <= a for b, a in hist))
        self.assertAlmostEqual(backend.skill, 1.0, places=3)


class TestBench(unittest.TestCase):
    def test_run_all(self):
        cfg = Config()
        engine = DramaEngine(cfg)
        results = run_all(engine)
        self.assertEqual(set(results.keys()), set(list_benchmarks()))
        for k, v in results.items():
            self.assertNotIn("error", v, "benchmark %s errored: %s" % (k, v))


if __name__ == "__main__":
    unittest.main()
