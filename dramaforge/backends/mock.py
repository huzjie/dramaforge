"""Mock backend: deterministic, trainable, zero-dependency.

The mock backend runs the *real* two-stage pipeline -- prosody -> emotion ->
acoustic -> RVQ codec -> vocoder -- but with deterministic parameters so every
run is reproducible. Its ``skill`` parameter models how faithfully the backend
obeys directives (the trainable signal), which drives the benchmark's directive
adherence metric.
"""
from .registry import register_backend
from ..utils.hash import stable_bool


@register_backend("mock")
class MockBackend:
    name = "mock"

    def __init__(self, config):
        self.cfg = config
        self.skill = config.model.skill

    def obedience(self, key):
        """Probability this backend obeys a directive key at current skill.

        Follows the project rule: ``boost = (skill - 0.5) * 2`` so skill=0.5
        gives a 0.5 (random) hit rate and skill=1.0 gives 1.0 (always obeys).
        """
        boost = (self.skill - 0.5) * 2.0
        p = 0.5 + 0.5 * boost
        return stable_bool(key, p)

    def synthesize(self, clean_text, tokens, attrs, turns, speakers, config):
        from ..engine.engine import AudioResult
        from ..engine.audio import crossfade, duration_s
        from ..prosody import ProsodyPredictor
        from ..emotion import EmotionEmbedder
        from ..acoustic import AcousticModel
        from ..vocoder import Vocoder
        from ..codec import RVQCodec

        sample_rate = config.acoustic.sample_rate
        prosody = ProsodyPredictor(frame_rate=config.prosody.frame_rate,
                                   pitch_bins=config.prosody.pitch_bins)
        emotion = EmotionEmbedder(embed_dim=config.emotion.embed_dim,
                                  n_emotions=config.emotion.n_emotions)
        acoustic = AcousticModel(n_mels=config.acoustic.n_mels,
                                 hop_length=config.acoustic.hop_length,
                                 sample_rate=sample_rate)
        vocoder = Vocoder(sample_rate=config.vocoder.sample_rate,
                          hop_length=config.vocoder.hop_length)
        codec = RVQCodec(n_quantizers=config.codec.n_quantizers,
                         codebook_size=config.codec.codebook_size,
                         dim=config.codec.mel_bins)

        all_codes = []
        segments = []
        obeyed = []
        for turn in turns:
            turn_attrs = attrs[turn.start_word:turn.end_word]
            spk = speakers.get(turn.speaker)
            pitch, energy, durs = prosody.predict(turn_attrs)
            embs = [emotion.embed(a.emotion) for a in turn_attrs]
            mel = acoustic.predict_frames(turn_attrs, pitch, energy, durs, spk, embs)
            codes = codec.encode_frames(mel)
            all_codes.extend(codes)
            wave = vocoder.mel_to_wave(mel)
            segments.append(wave)
            # obedience tracking per directive span
            for a in turn_attrs:
                obeyed.append(self.obedience("obey:%s:%s" % (a.text, a.emotion)))

        wave = segments[0] if segments else [0.0]
        for seg in segments[1:]:
            wave = crossfade(wave, seg, config.directive.crossfade_ms, sample_rate)

        adherence = (sum(1 for o in obeyed if o) / len(obeyed)) if obeyed else 0.0
        return AudioResult(
            waveform=wave,
            sample_rate=sample_rate,
            duration_s=duration_s(wave, sample_rate),
            codes=all_codes,
            metadata={
                "backend": "mock",
                "skill": round(self.skill, 4),
                "n_codes": len(all_codes),
                "directive_adherence": round(adherence, 4),
                "n_segments": len(segments),
            },
        )
