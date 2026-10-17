"""Audio analysis utilities."""
import unittest

from dramaforge.utils.audio_analysis import rms, zero_crossing_rate, energy_contour, spectral_centroid


class TestAnalysis(unittest.TestCase):
    def test_rms(self):
        self.assertAlmostEqual(rms([0.0, 0.0]), 0.0)

    def test_zcr(self):
        w = [1.0, -1.0, 1.0, -1.0]
        self.assertAlmostEqual(zero_crossing_rate(w), 1.0)

    def test_energy_contour(self):
        w = [0.5] * 8
        c = energy_contour(w, 4)
        self.assertEqual(len(c), 2)

    def test_spectral_centroid(self):
        mel = [[0.0, 0.0, 1.0]]
        self.assertAlmostEqual(spectral_centroid(mel)[0], 2.0)


if __name__ == "__main__":
    unittest.main()
