# API — speaker

- `speaker_embedding(name, dim=32)` — 确定性说话人嵌入
- `speaker_similarity(a, b)` — 嵌入 cosine
- `SpeakerLibrary(n_speakers, embed_dim, seed)` — 说话人库，`.get(name)` / `.closest(emb, k)` / `.list_speakers()`
- `plan_turns(words, attrs, default_voice, crossfade_ms)` — 多说话人分段
