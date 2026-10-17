# API — directive

- `Directive(start, end, emotion, voice, rate, pitch, emphasis, style)` — 区间指令
- `apply_directives(words, directives, defaults=None)` — 逐词解析属性，返回 `WordAttributes[]`
- `parse_bracketed(text, tokens=None)` — 解析 bracketed tags，返回 `(clean_text, directives)`
- `parse_natural(text, n_words)` — 自然语言执导 → `Directive[]`
- `parse_text(text)` — 合并解析，返回 `(clean_text, directives, tokens)`
