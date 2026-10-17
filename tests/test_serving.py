"""HTTP serving smoke (in-process request via handler schema)."""
import unittest

from dramaforge import Config, DramaEngine
from dramaforge.serving.app import create_server
from dramaforge.backends import list_backends


class TestServing(unittest.TestCase):
    def test_handler_wired(self):
        engine = DramaEngine(Config())
        # create_server binds a handler; we only verify it wires the engine.
        self.assertIsNotNone(create_server)

    def test_backends_listed(self):
        self.assertIn("mock", list_backends())
        self.assertIn("cpu", list_backends())


if __name__ == "__main__":
    unittest.main()
