"""Directive parsing and word-level attribute resolution."""
import unittest

from dramaforge.directive import parse_bracketed, apply_directives, parse_natural
from dramaforge.directive import Directive
from dramaforge.utils.text import tokenize_words


class TestBracketed(unittest.TestCase):
    def test_emotion_span(self):
        clean, directives = parse_bracketed("[emotion=angry]你好[/emotion] 世界")
        self.assertEqual(clean, "你好 世界")
        self.assertEqual(len(directives), 1)
        self.assertEqual(directives[0].emotion, "angry")

    def test_voice_span(self):
        clean, directives = parse_bracketed("[voice=alice]a[/voice] [voice=bob]b[/voice]")
        self.assertEqual([d.voice for d in directives], ["alice", "bob"])


class TestApply(unittest.TestCase):
    def test_word_level(self):
        words = tokenize_words("a b c d")
        d = [Directive(0, 2, emotion="angry"), Directive(2, 4, rate=1.5)]
        attrs = apply_directives(words, d)
        self.assertEqual(attrs[0].emotion, "angry")
        self.assertEqual(attrs[1].emotion, "angry")
        self.assertEqual(attrs[2].emotion, "neutral")
        self.assertEqual(attrs[2].rate, 1.5)


class TestNatural(unittest.TestCase):
    def test_emotion_keyword(self):
        ds = parse_natural("用愤怒的语气说", 5)
        self.assertEqual(ds[0].emotion, "angry")

    def test_rate_keyword(self):
        ds = parse_natural("语速快一点", 5)
        self.assertGreater(ds[0].rate, 1.0)


if __name__ == "__main__":
    unittest.main()
