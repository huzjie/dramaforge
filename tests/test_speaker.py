"""Speaker embeddings and library."""
import unittest

from dramaforge.speaker import SpeakerLibrary, speaker_embedding, speaker_similarity


class TestSpeaker(unittest.TestCase):
    def test_embedding_deterministic(self):
        a = speaker_embedding("alice", 32)
        b = speaker_embedding("alice", 32)
        self.assertEqual(a, b)

    def test_library(self):
        lib = SpeakerLibrary(n_speakers=8, embed_dim=32, seed=7)
        self.assertEqual(len(lib.list_speakers()), 8)
        self.assertIsNotNone(lib.get("alice"))
        # unknown name is synthesized deterministically
        self.assertIsNotNone(lib.get("zoe"))

    def test_separation(self):
        lib = SpeakerLibrary(n_speakers=8, embed_dim=32, seed=7)
        names = lib.list_speakers()
        sims = [speaker_similarity(lib.get(a).embedding, lib.get(b).embedding)
                for i, a in enumerate(names) for b in names[i + 1:]]
        self.assertTrue(all(s < 0.6 for s in sims))


if __name__ == "__main__":
    unittest.main()
