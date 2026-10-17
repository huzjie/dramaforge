"""Benchmark metric helpers (MOS / similarity / adherence)."""
from .vectors import cosine


def compute_mos(adherence):
    """Map directive adherence [0,1] to MOS [1,5]."""
    return 1.0 + 4.0 * max(0.0, min(1.0, adherence))


def compute_sim(emb_a, emb_b):
    """Speaker similarity = cosine of embeddings."""
    return cosine(emb_a, emb_b)


def compute_adherence(obeyed):
    """Fraction of directive draws obeyed."""
    if not obeyed:
        return 0.0
    return sum(1 for o in obeyed if o) / len(obeyed)
