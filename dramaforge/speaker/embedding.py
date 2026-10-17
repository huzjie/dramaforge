"""Deterministic speaker embeddings (mock stand-in for a speaker encoder).

In a real stack this is an ECAPA-TDNN / d-vector speaker encoder. Here we use
the shared stable-vector primitive keyed by speaker name, so two calls for the
same speaker are bit-identical and similarity is well-defined for the
benchmark's "speaker similarity" metric.
"""
from ..utils.hash import stable_vector
from ..utils.vectors import cosine


def speaker_embedding(name, dim=32):
    """Deterministic ``dim``-vector for a speaker ``name``."""
    return stable_vector("speaker:" + name, dim, -1.0, 1.0)


def speaker_similarity(a, b):
    """Cosine similarity between two speaker embeddings."""
    return cosine(a, b)
