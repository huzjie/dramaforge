"""RVQ codec efficiency benchmark.

Encodes a batch of synthetic acoustic frames and reports the token compression
(the audio-as-tokens story) plus the reconstruction error, which should shrink
as more quantizers are added.
"""
from .registry import register_benchmark
from ..codec import RVQCodec, reconstruction_error
from ..utils.hash import stable_vector


@register_benchmark("rvq_efficiency")
def run(engine, **kw):
    cfg = engine.config
    codec = RVQCodec(n_quantizers=cfg.codec.n_quantizers,
                     codebook_size=cfg.codec.codebook_size,
                     dim=cfg.codec.mel_bins)
    frames = [stable_vector("frame:%d" % i, cfg.codec.mel_bins) for i in range(40)]
    codes = codec.encode_frames(frames)
    decoded = codec.decode_frames(codes)
    err = reconstruction_error(frames, decoded)
    n_tokens = codec.token_count(len(frames))
    return {
        "n_frames": len(frames),
        "n_tokens": n_tokens,
        "tokens_per_frame": cfg.codec.n_quantizers,
        "reconstruction_rmse": round(err, 4),
    }
