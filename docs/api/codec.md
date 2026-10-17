# API — codec

- `Codebook(size, dim, key)` — 确定性码本，`.nearest(vec)` / `.decode(code)`
- `RVQCodec(n_quantizers, codebook_size, dim)` — 残差量化，`.encode_frames()` / `.decode_frames()` / `.token_count(n_frames)`
- `reconstruction_error(frames, decoded)` — 平均 RMSE
