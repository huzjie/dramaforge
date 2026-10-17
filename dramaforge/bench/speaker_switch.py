"""Multi-speaker switch benchmark.

Synthesizes a two-speaker dialogue and verifies the scene planner produced the
expected number of turns and that each turn's speaker matches the directive.
"""
from .registry import register_benchmark

DIALOGUE = ("[voice=alice]你好，请问是技术支持吗？[/voice] "
            "[voice=bob]是的，请问有什么可以帮您？[/voice] "
            "[voice=alice]我的账号登录不上了。[/voice]")


@register_benchmark("speaker_switch")
def run(engine, **kw):
    r = engine.synth(DIALOGUE)
    speakers = [t.speaker for t in r.turns]
    expected = ["alice", "bob", "alice"]
    correct = sum(1 for a, b in zip(speakers, expected) if a == b)
    return {
        "n_turns": len(r.turns),
        "speakers": speakers,
        "switch_correct": correct,
        "switch_accuracy": round(correct / len(expected), 4) if expected else 0.0,
    }
