"""Span-level directive model and word-level attribute resolution.

A ``Directive`` covers a half-open word-index range ``[start, end)`` and carries
the attributes that should govern that span: emotion, voice (speaker), rate,
pitch, emphasis and a free-form style tag. The whole point of "word-level
control" is that every word resolves its own attributes from the spans covering
it -- so ``[emotion=angry]really[/emotion] not again`` gives "really" an angry
rendition and "not again" the default.
"""
from dataclasses import dataclass, field


@dataclass
class Directive:
    start: int
    end: int
    emotion: str = "neutral"
    voice: str = ""
    rate: float = 1.0
    pitch: float = 1.0
    emphasis: float = 0.0
    style: str = ""

    def covers(self, i):
        return self.start <= i < self.end


@dataclass
class WordAttributes:
    text: str
    emotion: str = "neutral"
    voice: str = ""
    rate: float = 1.0
    pitch: float = 1.0
    emphasis: float = 0.0
    style: str = ""

    def as_dict(self):
        return {
            "text": self.text,
            "emotion": self.emotion,
            "voice": self.voice,
            "rate": self.rate,
            "pitch": self.pitch,
            "emphasis": self.emphasis,
            "style": self.style,
        }


def apply_directives(words, directives, defaults=None):
    """Resolve per-word attributes from a list of span directives.

    ``defaults`` is an optional dict with keys ``emotion/voice/rate/pitch/
    emphasis/style``; values missing from any covering directive fall back to
    these, then to module-level defaults.

    Overlap policy: later directives in the list win (last-write-wins), which
    makes stacking natural-language directions on top of tag directions
    predictable.
    """
    d = {
        "emotion": "neutral",
        "voice": "",
        "rate": 1.0,
        "pitch": 1.0,
        "emphasis": 0.0,
        "style": "",
    }
    if defaults:
        d.update({k: v for k, v in defaults.items() if v not in (None, "")})

    attrs = []
    for i, w in enumerate(words):
        a = WordAttributes(text=w, **d)
        for dv in directives:
            if dv.covers(i):
                if dv.emotion:
                    a.emotion = dv.emotion
                if dv.voice:
                    a.voice = dv.voice
                if dv.rate != 1.0:
                    a.rate = dv.rate
                if dv.pitch != 1.0:
                    a.pitch = dv.pitch
                if dv.emphasis != 0.0:
                    a.emphasis = dv.emphasis
                if dv.style:
                    a.style = dv.style
        attrs.append(a)
    return attrs
