"""Emotion embeddings.

Emotion is encoded as a deterministic ``embed_dim`` vector conditioned on the
emotion label. The acoustic model later conditions on this vector, so "angry"
and "gentle" steer synthesis in different directions. A real stack uses a
learned emotion encoder; here the stable-vector primitive keeps everything
reproducible for benchmarks.
"""
from ..utils.hash import stable_vector

EMOTIONS = [
    "neutral", "happy", "sad", "angry",
    "gentle", "excited", "fearful", "surprised",
]


class EmotionEmbedder:
    def __init__(self, embed_dim=16, n_emotions=8):
        self.embed_dim = embed_dim
        self.emotions = EMOTIONS[:n_emotions]
        self._cache = {}

    def embed(self, emotion):
        emotion = emotion if emotion in self.emotions else "neutral"
        if emotion not in self._cache:
            self._cache[emotion] = stable_vector("emotion:" + emotion, self.embed_dim)
        return self._cache[emotion]

    def onehot(self, emotion):
        emotion = emotion if emotion in self.emotions else "neutral"
        idx = self.emotions.index(emotion)
        v = [0.0] * len(self.emotions)
        v[idx] = 1.0
        return v
