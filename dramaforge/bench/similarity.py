"""Speaker similarity benchmark.

Measures how well speaker embeddings separate in the library: the average
pairwise cosine similarity should be near 0 (orthogonal, well-separated voices)
and the self-similarity exactly 1.0. This is a real, measurable property of the
deterministic speaker encoder.
"""
from .registry import register_benchmark
from ..speaker.embedding import speaker_similarity


@register_benchmark("speaker_similarity")
def run(engine, **kw):
    names = engine.speakers.list_speakers()
    embs = {n: engine.speakers.get(n).embedding for n in names}
    self_sim = [speaker_similarity(embs[n], embs[n]) for n in names]
    pairs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            pairs.append(speaker_similarity(embs[a], embs[b]))
    avg_cross = sum(pairs) / len(pairs) if pairs else 0.0
    return {
        "n_speakers": len(names),
        "self_similarity": round(sum(self_sim) / len(self_sim), 4) if self_sim else 0.0,
        "avg_cross_similarity": round(avg_cross, 4),
    }
