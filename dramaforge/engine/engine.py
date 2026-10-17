"""DramaEngine: orchestrates directive -> synthesis -> audio result.

The engine is the single entry point a caller uses. It parses direction, resolves
word-level attributes, plans speaker turns, and delegates waveform generation to
a backend. The result bundles the waveform with enough metadata (directives,
turns, RVQ codes, prosody) to support the benchmark metrics.
"""
from dataclasses import dataclass, field

from ..config import Config, load_config
from ..directive import parse_text, apply_directives, parse_natural
from ..speaker import SpeakerLibrary
from ..speaker.scene import plan_turns
from ..backends import get_backend


@dataclass
class AudioResult:
    waveform: list = field(default_factory=list)
    sample_rate: int = 24000
    duration_s: float = 0.0
    clean_text: str = ""
    tokens: list = field(default_factory=list)
    word_attrs: list = field(default_factory=list)
    directives: list = field(default_factory=list)
    turns: list = field(default_factory=list)
    codes: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def as_dict(self):
        return {
            "sample_rate": self.sample_rate,
            "duration_s": round(self.duration_s, 3),
            "clean_text": self.clean_text,
            "n_tokens": len(self.tokens),
            "n_turns": len(self.turns),
            "n_codes": len(self.codes),
            "metadata": self.metadata,
        }


class DramaEngine:
    def __init__(self, config=None, backend=None):
        self.config = config if config is not None else Config()
        self.speakers = SpeakerLibrary(
            n_speakers=self.config.speaker.n_speakers,
            embed_dim=self.config.speaker.embed_dim,
            seed=self.config.speaker.seed,
        )
        self.backend = backend if backend is not None else get_backend(
            self.config.model.name, self.config)

    def synth(self, text, direction=None, voice=None, emotion=None):
        """Synthesize ``text`` under optional direction, default voice/emotion.

        ``direction`` may be a natural-language instruction or additional
        bracketed tags. ``voice`` / ``emotion`` set whole-text defaults.
        """
        clean_text, directives, tokens = parse_text(text)

        defaults = {
            "emotion": emotion or self.config.directive.default_emotion,
            "voice": voice or self.config.directive.default_voice,
            "rate": self.config.directive.default_rate,
            "pitch": self.config.directive.default_pitch,
            "emphasis": self.config.directive.default_emphasis,
            "style": "",
        }

        if direction:
            nat = parse_natural(direction, len(tokens))
            directives = directives + nat

        attrs = apply_directives(tokens, directives, defaults)
        turns = plan_turns(tokens, attrs, defaults["voice"],
                           self.config.directive.crossfade_ms)

        result = self.backend.synthesize(
            clean_text=clean_text, tokens=tokens, attrs=attrs, turns=turns,
            speakers=self.speakers, config=self.config,
        )
        result.clean_text = clean_text
        result.tokens = tokens
        result.word_attrs = attrs
        result.directives = directives
        result.turns = turns
        return result

    def serve_ready(self):
        return {"engine": "dramaforge", "backend": self.config.model.name}
