"""End-to-end synthesis smoke."""
import unittest
import tempfile
import os

from dramaforge import Config, DramaEngine
from dramaforge.engine.audio import save_wav, duration_s


class TestEngine(unittest.TestCase):
    def test_synth(self):
        cfg = Config()
        cfg.codec.n_quantizers = 2
        cfg.codec.codebook_size = 64
        cfg.acoustic.n_mels = 16
        cfg.speaker.n_speakers = 4
        engine = DramaEngine(cfg)
        r = engine.synth("你好世界。", direction="用开心的语气说")
        self.assertGreater(len(r.waveform), 0)
        self.assertGreater(r.duration_s, 0.0)
        self.assertEqual(len(r.turns), 1)

    def test_save_wav(self):
        engine = DramaEngine(Config())
        r = engine.synth("测试")
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "out.wav")
            save_wav(p, r.waveform, r.sample_rate)
            self.assertTrue(os.path.exists(p))
            self.assertGreater(os.path.getsize(p), 44)


if __name__ == "__main__":
    unittest.main()
