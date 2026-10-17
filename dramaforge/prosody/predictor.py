"""Prosody prediction.

Prosody (pitch contour, energy contour, per-word duration) is what makes speech
sound human rather than robotic. The predictor takes the word attributes
(emotion / rate / pitch / emphasis) and produces frame-level trajectories.

This is a deterministic reference: pitch follows the word's ``pitch`` attribute
with emotion- and emphasis-driven perturbations; energy is driven by
``emphasis`` and the emotion's typical loudness; duration scales with ``rate``.
A real stack swaps this for a learned prosody model conditioned on speaker and
emotion embeddings.
"""
import math

from ..utils.hash import stable_float

EMOTION_PROFILE = {
    "neutral": {"pitch_shift": 0.0, "energy": 0.5, "rate_shift": 0.0},
    "happy": {"pitch_shift": 0.15, "energy": 0.7, "rate_shift": 0.08},
    "sad": {"pitch_shift": -0.12, "energy": 0.35, "rate_shift": -0.12},
    "angry": {"pitch_shift": 0.05, "energy": 0.85, "rate_shift": 0.1},
    "gentle": {"pitch_shift": -0.05, "energy": 0.4, "rate_shift": -0.1},
    "excited": {"pitch_shift": 0.2, "energy": 0.8, "rate_shift": 0.15},
    "fearful": {"pitch_shift": 0.1, "energy": 0.45, "rate_shift": 0.05},
    "surprised": {"pitch_shift": 0.25, "energy": 0.75, "rate_shift": 0.12},
}


class ProsodyPredictor:
    def __init__(self, frame_rate=50, pitch_bins=12):
        self.frame_rate = frame_rate
        self.pitch_bins = pitch_bins

    def word_profile(self, attr):
        prof = EMOTION_PROFILE.get(attr.emotion, EMOTION_PROFILE["neutral"])
        pitch = (attr.pitch + prof["pitch_shift"]) if attr.pitch != 1.0 else (1.0 + prof["pitch_shift"])
        energy = prof["energy"] + 0.35 * attr.emphasis
        energy = max(0.05, min(1.0, energy))
        rate = attr.rate * (1.0 + prof["rate_shift"]) if attr.rate != 1.0 else (1.0 + prof["rate_shift"])
        duration = max(1, int(round(self.frame_rate * 0.12 / max(0.3, rate))))
        return pitch, energy, duration

    def predict(self, attrs):
        """Return (pitch_curve, energy_curve, durations) for a list of words."""
        pitch_curve = []
        energy_curve = []
        durations = []
        for a in attrs:
            pitch, energy, dur = self.word_profile(a)
            durations.append(dur)
            for f in range(dur):
                wob = stable_float("pros:%s:%d" % (a.text, f), -0.04, 0.04)
                pitch_curve.append(max(0.2, pitch + wob))
                energy_curve.append(energy)
        return pitch_curve, energy_curve, durations
