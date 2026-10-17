# API — engine

- `DramaEngine(config=None, backend=None)` — `.synth(text, direction, voice, emotion)` 返回 `AudioResult`
- `AudioResult` — `.waveform` / `.sample_rate` / `.duration_s` / `.word_attrs` / `.turns` / `.codes` / `.metadata` / `.as_dict()`
- `audio.save_wav(path, wave, sr)` / `normalize_wave` / `crossfade` / `concat` / `rms` / `duration_s`
