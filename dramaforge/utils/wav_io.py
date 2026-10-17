"""WAV read/write (stdlib only), including a reader."""
import struct
import wave


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        n = w.getnframes()
        sr = w.getframerate()
        raw = w.readframes(n)
    samples = list(struct.unpack("<%dh" % n, raw))
    return samples, sr


def write_wav(path, samples, sample_rate=24000):
    from ..engine.audio import save_wav
    return save_wav(path, samples, sample_rate)
