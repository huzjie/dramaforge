"""Configuration dataclass + zero-dependency YAML loader.

When PyYAML is absent (the managed Python has no third-party deps), we fall back
to :mod:`dramaforge.utils.yamlish`.
"""
from dataclasses import dataclass, field
from pathlib import Path

from .utils.yamlish import parse

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


@dataclass
class DirectiveConfig:
    default_emotion: str = "neutral"
    default_voice: str = "narrator"
    default_rate: float = 1.0
    default_pitch: float = 1.0
    default_emphasis: float = 0.0
    crossfade_ms: float = 30.0


@dataclass
class SpeakerConfig:
    n_speakers: int = 8
    embed_dim: int = 32
    seed: int = 7


@dataclass
class CodecConfig:
    n_quantizers: int = 4
    codebook_size: int = 256
    mel_bins: int = 32


@dataclass
class ProsodyConfig:
    frame_rate: int = 50
    pitch_bins: int = 12


@dataclass
class EmotionConfig:
    embed_dim: int = 16
    n_emotions: int = 8


@dataclass
class AcousticConfig:
    sample_rate: int = 24000
    n_mels: int = 32
    hop_length: int = 256


@dataclass
class VocoderConfig:
    sample_rate: int = 24000
    hop_length: int = 256


@dataclass
class ModelConfig:
    name: str = "mock"
    skill: float = 0.5
    sample_rate: int = 24000


@dataclass
class ServingConfig:
    host: str = "127.0.0.1"
    port: int = 8000


@dataclass
class Config:
    directive: DirectiveConfig = field(default_factory=DirectiveConfig)
    speaker: SpeakerConfig = field(default_factory=SpeakerConfig)
    codec: CodecConfig = field(default_factory=CodecConfig)
    prosody: ProsodyConfig = field(default_factory=ProsodyConfig)
    emotion: EmotionConfig = field(default_factory=EmotionConfig)
    acoustic: AcousticConfig = field(default_factory=AcousticConfig)
    vocoder: VocoderConfig = field(default_factory=VocoderConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    serving: ServingConfig = field(default_factory=ServingConfig)
    seed: int = 42

    @classmethod
    def from_dict(cls, d):
        def i(v, default):
            return int(v) if v is not None else default

        def f(v, default):
            return float(v) if v is not None else default

        def s(v, default):
            return str(v) if v is not None else default

        directive = d.get("directive", {}) or {}
        speaker = d.get("speaker", {}) or {}
        codec = d.get("codec", {}) or {}
        prosody = d.get("prosody", {}) or {}
        emotion = d.get("emotion", {}) or {}
        acoustic = d.get("acoustic", {}) or {}
        vocoder = d.get("vocoder", {}) or {}
        model = d.get("model", {}) or {}
        serving = d.get("serving", {}) or {}
        return cls(
            directive=DirectiveConfig(
                default_emotion=s(directive.get("default_emotion"), "neutral"),
                default_voice=s(directive.get("default_voice"), "narrator"),
                default_rate=f(directive.get("default_rate"), 1.0),
                default_pitch=f(directive.get("default_pitch"), 1.0),
                default_emphasis=f(directive.get("default_emphasis"), 0.0),
                crossfade_ms=f(directive.get("crossfade_ms"), 30.0),
            ),
            speaker=SpeakerConfig(
                n_speakers=i(speaker.get("n_speakers"), 8),
                embed_dim=i(speaker.get("embed_dim"), 32),
                seed=i(speaker.get("seed"), 7),
            ),
            codec=CodecConfig(
                n_quantizers=i(codec.get("n_quantizers"), 4),
                codebook_size=i(codec.get("codebook_size"), 256),
                mel_bins=i(codec.get("mel_bins"), 32),
            ),
            prosody=ProsodyConfig(
                frame_rate=i(prosody.get("frame_rate"), 50),
                pitch_bins=i(prosody.get("pitch_bins"), 12),
            ),
            emotion=EmotionConfig(
                embed_dim=i(emotion.get("embed_dim"), 16),
                n_emotions=i(emotion.get("n_emotions"), 8),
            ),
            acoustic=AcousticConfig(
                sample_rate=i(acoustic.get("sample_rate"), 24000),
                n_mels=i(acoustic.get("n_mels"), 32),
                hop_length=i(acoustic.get("hop_length"), 256),
            ),
            vocoder=VocoderConfig(
                sample_rate=i(vocoder.get("sample_rate"), 24000),
                hop_length=i(vocoder.get("hop_length"), 256),
            ),
            model=ModelConfig(
                name=s(model.get("name"), "mock"),
                skill=f(model.get("skill"), 0.5),
                sample_rate=i(model.get("sample_rate"), 24000),
            ),
            serving=ServingConfig(
                host=s(serving.get("host"), "127.0.0.1"),
                port=i(serving.get("port"), 8000),
            ),
            seed=i(d.get("seed"), 42),
        )


def load_config(path=None):
    if path is None:
        return Config()
    p = Path(path)
    if not p.exists():
        return Config()
    text = p.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text) or {}
    else:
        data = parse(text)
    return Config.from_dict(data)
