"""SpeakerLibrary: a deterministic roster of speakers.

Speakers are generated from a seed and looked up by name; unknown names are
synthesized deterministically too (so the same name always yields the same
voice, making scripts reproducible).
"""
from .speaker import Speaker
from .embedding import speaker_embedding
from ..utils.hash import stable_vector, stable_float


class SpeakerLibrary:
    def __init__(self, n_speakers=8, embed_dim=32, seed=7):
        self.embed_dim = embed_dim
        self.seed = seed
        self.speakers = {}
        self._default_names = [
            "narrator", "alice", "bob", "carol", "dave", "erin", "frank", "grace",
            "henry", "ivy", "jack", "kate", "leo", "mia", "noah", "olivia",
            "paul", "quin", "rose", "sam",
        ]
        for i in range(n_speakers):
            name = self._default_names[i % len(self._default_names)]
            if i >= len(self._default_names):
                name = name + str(i // len(self._default_names))
            self._register(name)

    def _register(self, name):
        if name in self.speakers:
            return self.speakers[name]
        emb = speaker_embedding(name, self.embed_dim)
        timbre = stable_vector("timbre:" + name, 8, -1.0, 1.0)
        gender = "female" if stable_float("gender:" + name) < 0.5 else "male"
        spk = Speaker(name=name, embedding=emb, timbre=timbre, gender=gender,
                      description="deterministic mock speaker")
        self.speakers[name] = spk
        return spk

    def get(self, name):
        """Return a speaker by name, creating it deterministically if unknown."""
        if not name:
            return None
        return self.speakers.get(name) or self._register(name)

    def closest(self, embedding, k=1):
        """Top-k speakers by cosine similarity to ``embedding``."""
        from .embedding import speaker_similarity
        scored = sorted(
            ((speaker_similarity(embedding, s.embedding), s.name) for s in self.speakers.values()),
            key=lambda x: (-x[0], x[1]),
        )
        return [name for _, name in scored[:k]]

    def list_speakers(self):
        return sorted(self.speakers.keys())
