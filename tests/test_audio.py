"""Audio I/O and utilities."""
import unittest
import tempfile
import os

from dramaforge.engine.audio import normalize_wave, crossfade, concat, rms, save_wav
from dramaforge.utils.wav_io import read_wav


class TestAudio(unittest.TestCase):
    def test_normalize(self):
        w = normalize_wave([0.0, 0.5, 0.2])
        self.assertLessEqual(max(abs(x) for x in w), 0.95)

    def test_crossfade_length(self):
        a = [1.0] * 100
        b = [0.0] * 100
        c = crossfade(a, b, 10, 1000)
        self.assertEqual(len(c), 200 - 10)

    def test_wav_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.wav")
            save_wav(p, [0.0, 0.1, -0.1, 0.05], 24000)
            samples, sr = read_wav(p)
            self.assertEqual(sr, 24000)
            self.assertEqual(len(samples), 4)


if __name__ == "__main__":
    unittest.main()
