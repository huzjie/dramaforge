"""MOS (mean opinion score) benchmark.

A stand-in for a human/subjective listener study: MOS is derived from directive
adherence and the engine's skill. Perfect adherence -> MOS 5.0; random -> 3.0.
In a real system this would be scored by a learned MOS predictor or a human
panel.
"""
from .registry import register_benchmark


@register_benchmark("mos")
def run(engine, **kw):
    r = engine.synth("这是一段用于自然度评测的合成语音。")
    adherence = r.metadata.get("directive_adherence", 0.5)
    mos = 1.0 + 4.0 * adherence
    return {
        "mos": round(mos, 3),
        "duration_s": round(r.duration_s, 3),
    }
