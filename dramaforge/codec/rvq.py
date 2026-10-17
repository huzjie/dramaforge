"""Residual vector quantization (RVQ).

Modern neural audio codecs (SoundStream, EnCodec, and the Drama-3 style codecs)
represent audio as a *sequence of multi-level discrete codes* rather than raw
samples. RVQ is the core trick: the first codebook captures the coarse shape,
each subsequent codebook quantizes the *residual* left over from the previous
level, so fidelity scales with the number of quantizers.

This module is a pure-Python reference: deterministic codebooks + nearest
neighbour search. It is the mechanism the mock backend uses to demonstrate
"audio as a short token sequence".
"""
import math

from ..utils.hash import stable_vector


class Codebook:
    def __init__(self, size, dim, key="cb"):
        self.size = size
        self.dim = dim
        self.entries = [stable_vector("%s:%d" % (key, i), dim, -1.0, 1.0)
                        for i in range(size)]

    def nearest(self, vec):
        best = -1
        best_d = float("inf")
        for i, e in enumerate(self.entries):
            d = sum((a - b) * (a - b) for a, b in zip(vec, e))
            if d < best_d:
                best_d = d
                best = i
        return best

    def decode(self, code):
        return list(self.entries[code])


class RVQCodec:
    def __init__(self, n_quantizers=4, codebook_size=256, dim=32):
        self.n_quantizers = n_quantizers
        self.dim = dim
        self.codebooks = [Codebook(codebook_size, dim, key="rvq:%d" % q)
                          for q in range(n_quantizers)]

    def encode_frame(self, vec):
        residual = list(vec)
        codes = []
        for cb in self.codebooks:
            c = cb.nearest(residual)
            codes.append(c)
            recon = cb.decode(c)
            residual = [r - e for r, e in zip(residual, recon)]
        return codes

    def decode_frame(self, codes):
        out = [0.0] * self.dim
        for c, cb in zip(codes, self.codebooks):
            e = cb.decode(c)
            out = [o + x for o, x in zip(out, e)]
        return out

    def encode_frames(self, frames):
        return [self.encode_frame(f) for f in frames]

    def decode_frames(self, codes):
        return [self.decode_frame(c) for c in codes]

    def token_count(self, n_frames):
        return n_frames * self.n_quantizers


def reconstruction_error(frames, decoded):
    """Mean squared reconstruction error between original and decoded frames."""
    n = 0
    total = 0.0
    for f, d in zip(frames, decoded):
        for a, b in zip(f, d):
            total += (a - b) * (a - b)
            n += 1
    if n == 0:
        return 0.0
    return math.sqrt(total / n)
