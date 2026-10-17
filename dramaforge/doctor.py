"""Self-check: instantiate every component and run a synthesis smoke test."""
import json

from .backends import list_backends
from .bench import list_benchmarks


def run_doctor(cfg, engine=None):
    if engine is None:
        from .engine import DramaEngine
        engine = DramaEngine(cfg)

    print("== dramaforge doctor ==")
    print("backends:   %s" % ", ".join(list_backends()))
    print("benchmarks: %s" % ", ".join(list_benchmarks()))

    # components
    from .codec import RVQCodec
    from .prosody import ProsodyPredictor
    from .emotion import EmotionEmbedder
    from .acoustic import AcousticModel
    from .vocoder import Vocoder
    from .directive import parse_text
    from .speaker import SpeakerLibrary

    codec = RVQCodec(cfg.codec.n_quantizers, cfg.codec.codebook_size, cfg.codec.mel_bins)
    print("codec:      %d quantizers x %d codes (dim %d)"
          % (cfg.codec.n_quantizers, cfg.codec.codebook_size, cfg.codec.mel_bins))

    prosody = ProsodyPredictor(cfg.prosody.frame_rate, cfg.prosody.pitch_bins)
    emotion = EmotionEmbedder(cfg.emotion.embed_dim, cfg.emotion.n_emotions)
    acoustic = AcousticModel(cfg.acoustic.n_mels, cfg.acoustic.hop_length, cfg.acoustic.sample_rate)
    vocoder = Vocoder(cfg.vocoder.sample_rate, cfg.vocoder.hop_length)
    speakers = SpeakerLibrary(cfg.speaker.n_speakers, cfg.speaker.embed_dim, cfg.speaker.seed)
    print("speakers:   %d voices" % len(speakers.list_speakers()))

    # RVQ round-trip
    from .utils.hash import stable_vector
    from .codec import reconstruction_error
    frames = [stable_vector("doc:%d" % i, cfg.codec.mel_bins) for i in range(16)]
    codes = codec.encode_frames(frames)
    dec = codec.decode_frames(codes)
    print("rvq:        %d frames -> %d tokens, rmse %.4f"
          % (len(frames), codec.token_count(len(frames)), reconstruction_error(frames, dec)))

    # directive parse smoke
    clean, directives, tokens = parse_text("[emotion=angry]你好[/emotion] 世界")
    print("directive:  %d tokens, %d directives" % (len(tokens), len(directives)))

    # emotion embed smoke
    e = emotion.embed("angry")
    print("emotion:    embed dim %d, onehot len %d" % (len(e), len(emotion.onehot("angry"))))

    # full synthesis smoke
    r = engine.synth("你好，欢迎使用 dramaforge 可执导语音合成引擎。",
                     direction="用温柔的语气说")
    print("synth:      %.3fs audio, %d samples, %d codes" %
          (r.duration_s, len(r.waveform), len(r.codes)))
    print(json.dumps(r.metadata, ensure_ascii=False))
    print("== doctor OK ==")


if __name__ == "__main__":
    from .config import load_config
    import sys
    cfg = load_config(sys.argv[1] if len(sys.argv) > 1 else None)
    run_doctor(cfg)
