"""Prosody / acoustic / vocoder shape checks."""
import unittest

from dramaforge.directive import Directive, apply_directives
from dramaforge.utils.text import tokenize_words
from dramaforge.prosody import ProsodyPredictor
from dramaforge.acoustic import AcousticModel
from dramaforge.vocoder import Vocoder
from dramaforge.emotion import EmotionEmbedder


class TestPipeline(unittest.TestCase):
    def test_prosody(self):
        words = tokenize_words("测试文本")
        attrs = apply_directives(words, [Directive(0, len(words), emotion="happy")])
        p = ProsodyPredictor(frame_rate=50, pitch_bins=12)
        pitch, energy, dur = p.predict(attrs)
        self.assertEqual(len(pitch), sum(dur))
        self.assertEqual(len(energy), sum(dur))
        self.assertEqual(len(dur), len(words))

    def test_acoustic(self):
        words = tokenize_words("测试")
        attrs = apply_directives(words, [])
        p = ProsodyPredictor(50, 12)
        pitch, energy, dur = p.predict(attrs)
        em = EmotionEmbedder(16, 8)
        ac = AcousticModel(n_mels=16, hop_length=256, sample_rate=24000)
        mel = ac.predict_frames(attrs, pitch, energy, dur, None, [em.embed("neutral")])
        self.assertGreater(len(mel), 0)
        self.assertEqual(len(mel[0]), 16)

    def test_vocoder(self):
        ac = AcousticModel(n_mels=16, hop_length=128, sample_rate=24000)
        mel = [[0.0] * 16 for _ in range(4)]
        mel[0][8] = 1.0
        voc = Vocoder(sample_rate=24000, hop_length=128)
        wave = voc.mel_to_wave(mel)
        self.assertEqual(len(wave), 4 * 128)


if __name__ == "__main__":
    unittest.main()
