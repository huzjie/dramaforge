"""Directive adherence benchmark.

Synthesizes a script with several emotion / rate / pitch directives and reads
back the mock backend's adherence rate (fraction of directive-keyed draws that
were obeyed). Because the mock's obedience is skill-driven, adherence climbs
0.5 -> 1.0 as skill trains.
"""
from .registry import register_benchmark

SCRIPT = ("[emotion=angry]我真的受够了！[/emotion] "
          "然后她[rate=0.8]慢慢地说[/rate]，"
          "[emotion=gentle]没关系，我们慢慢来。[/emotion]")


@register_benchmark("directive_adherence")
def run(engine, **kw):
    r = engine.synth(SCRIPT)
    return {
        "adherence": round(r.metadata.get("directive_adherence", 0.0), 4),
        "n_directives": len(r.directives),
        "n_tokens": len(r.tokens),
    }
