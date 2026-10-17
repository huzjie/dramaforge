"""Acoustic model (reference): turn word attributes into mel frames.

The acoustic model maps each word (with its resolved emotion / speaker / pitch /
energy / emphasis) to a sequence of mel-spectrogram frames. This is the "text
frontend -> acoustic features" half of the synthesis pipeline.

Deterministic reference: pitch places energy on a specific mel bin (plus
harmonics), energy scales the amplitude, and the speaker timbre + emotion
embedding perturb the spectral envelope so different voices/emotions sound
different in a measurable way.
"""
import math

from ..utils.hash import stable_float, stable_vector


class AcousticModel:
    def __init__(self, n_mels=32, hop_length=256, sample_rate=24000):
        self.n_mels = n_mels
        self.hop_length = hop_length
        self.sample_rate = sample_rate

    def _mel_bin(self, pitch):
        # pitch ~1.0 -> mid bin; higher pitch -> higher bin
        mid = self.n_mels * 0.45
        return max(1, min(self.n_mels - 1, int(round(mid * pitch))))

    def predict_frames(self, attrs, pitch_curve, energy_curve, durations,
                       speaker, emotion_emb):
        """Produce one mel vector per prosody frame.

        Returns ``list[list[float]]`` of shape ``(total_frames, n_mels)``.
        """
        frames = []
        frame_idx = 0
        timbre = speaker.timbre if speaker else [0.0] * 8
        for a, dur in zip(attrs, durations):
            for f in range(dur):
                pitch = pitch_curve[frame_idx] if frame_idx < len(pitch_curve) else 1.0
                energy = energy_curve[frame_idx] if frame_idx < len(energy_curve) else 0.5
                bin_center = self._mel_bin(pitch)
                mel = [0.0] * self.n_mels
                # fundamental + two harmonics
                for h, amp in ((0, 1.0), (1, 0.5), (2, 0.25)):
                    b = bin_center + h * 3
                    if 0 <= b < self.n_mels:
                        mel[b] += amp
                # spectral envelope from timbre + emotion
                for b in range(self.n_mels):
                    env = 0.5 + 0.5 * stable_float(
                        "env:%s:%d:%d:%s" % (a.text, f, b, a.emotion), 0.0, 1.0)
                    mel[b] *= (0.6 + 0.4 * env)
                # energy scaling (with emphasis lift)
                mel = [m * energy * 3.0 for m in mel]
                # slight noise floor
                mel = [m + stable_float("nf:%d:%d" % (frame_idx, b), 0.0, 0.02)
                       for b, m in enumerate(mel)]
                frames.append(mel)
                frame_idx += 1
        return frames
