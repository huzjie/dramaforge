"""Vocoder (reference): mel frames -> waveform samples.

The vocoder is the "acoustic features -> audio" half of the pipeline. This
reference implementation is a simplified additive synthesis: each mel frame is
interpreted as a spectrum whose dominant bin selects a fundamental frequency,
and a sine + harmonics + noise burst is emitted for one hop of samples.

It produces a real, audible-ish waveform cheaply and deterministically -- enough
to exercise the full text -> directive -> prosody -> acoustic -> waveform chain
with zero dependencies and no GPU.
"""
import math

from ..utils.hash import stable_float


class Vocoder:
    def __init__(self, sample_rate=24000, hop_length=256):
        self.sample_rate = sample_rate
        self.hop_length = hop_length

    def _fundamental(self, mel):
        # dominant bin -> frequency (map bin 0..n_mels to ~80..600 Hz log-ish)
        n = len(mel)
        peak = max(range(n), key=lambda i: mel[i])
        frac = peak / max(1, n - 1)
        return 80.0 * (600.0 / 80.0) ** frac

    def mel_to_wave(self, mel_frames):
        """Convert mel frames to a flat list of float samples in [-1, 1]."""
        wave = []
        for mel in mel_frames:
            f0 = self._fundamental(mel)
            amp = max(mel) / 3.0
            amp = min(1.0, amp)
            for i in range(self.hop_length):
                t = i / self.sample_rate
                s = 0.0
                # fundamental + 2 harmonics
                for h in (1.0, 2.0, 3.0):
                    s += math.sin(2 * math.pi * f0 * h * t) / h
                # breath noise
                noise = stable_float("nz:%d" % i, -1.0, 1.0) * 0.05
                # simple fade in/out per hop to avoid clicks
                env = 0.5 - 0.5 * math.cos(2 * math.pi * i / self.hop_length)
                wave.append((s * amp * 0.6 + noise) * env)
        return wave
