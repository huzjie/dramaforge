"""Minimal text utilities (no external tokenizers)."""


def tokenize_words(text):
    """Split into words, keeping CJK runs as single tokens and punctuation.

    Deterministic and lossless enough for span alignment: a word-level directive
    must be able to address every token this function returns.
    """
    tokens = []
    buf = []
    for ch in text:
        if ch.isalnum():
            buf.append(ch)
        else:
            if buf:
                tokens.append("".join(buf))
                buf = []
            if not ch.isspace():
                tokens.append(ch)
    if buf:
        tokens.append("".join(buf))
    return tokens


def word_counts(text):
    return max(1, len(tokenize_words(text)))
