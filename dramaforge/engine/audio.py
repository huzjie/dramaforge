"""Tiny audio utilities (standard library only)."""
import math
import struct
import wave


def normalize_wave(wave, peak=0.95):
    m = max((abs(x) for x in wave), default=0.0)
    if m == 0:
        return list(wave)
    s = peak / m
    return [x * s for x in wave]


def rms(wave):
    if not wave:
        return 0.0
    return math.sqrt(sum(x * x for x in wave) / len(wave))


def duration_s(wave, sample_rate):
    return len(wave) / sample_rate


def concat(waves):
    out = []
    for w in waves:
        out.extend(w)
    return out


def crossfade(a, b, ms, sample_rate):
    n = int(sample_rate * ms / 1000.0)
    if n <= 0 or len(a) < n or len(b) < n:
        return concat([a, b])
    n = min(n, len(a), len(b))
    out = list(a[:-n])
    for i in range(n):
        w = i / n
        out.append(a[len(a) - n + i] * (1 - w) + b[i] * w)
    out.extend(b[n:])
    return out


def save_wav(path, samples, sample_rate=24000):
    """Write a 16-bit PCM mono WAV file using only the stdlib."""
    samples = normalize_wave(samples, 0.95)
    frames = bytearray()
    for x in samples:
        v = int(max(-1.0, min(1.0, x)) * 32767)
        frames += struct.pack("<h", v)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(bytes(frames))
    return str(path)
