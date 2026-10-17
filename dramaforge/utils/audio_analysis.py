"""Audio analysis utilities (stdlib only): pitch, energy, spectral stats."""
import math


def rms(wave):
    if not wave:
        return 0.0
    return math.sqrt(sum(x * x for x in wave) / len(wave))


def zero_crossing_rate(wave):
    if len(wave) < 2:
        return 0.0
    return sum(1 for a, b in zip(wave, wave[1:]) if a * b < 0) / (len(wave) - 1)


def energy_contour(wave, frame_size):
    return [rms(wave[i:i + frame_size])
            for i in range(0, len(wave), frame_size)]


def autocorr_pitch(wave, sample_rate, lo_hz=70.0, hi_hz=400.0):
    """Rough autocorrelation pitch estimate in Hz (or None if unclear)."""
    lo_lag = int(sample_rate / hi_hz)
    hi_lag = int(sample_rate / lo_hz)
    n = len(wave)
    if n < hi_lag * 2:
        return None
    best_lag = None
    best = -1.0
    for lag in range(lo_lag, min(hi_lag, n // 2)):
        s = sum(wave[i] * wave[i + lag] for i in range(0, n - lag))
        if s > best:
            best = s
            best_lag = lag
    if best_lag is None:
        return None
    return sample_rate / best_lag


def spectral_centroid(mel_frames):
    """Weighted-mean bin index per frame -> list of floats."""
    out = []
    for mel in mel_frames:
        s = sum(mel)
        if s == 0:
            out.append(0.0)
            continue
        out.append(sum(i * v for i, v in enumerate(mel)) / s)
    return out
