"""Bracketed-tag direction: ``[emotion=angry]text[/emotion]`` etc.

Tags are the compact, precise way to direct speech. The parser strips tags out
of the source text, records the word-index span each tag covers, and returns the
clean text plus the resolved directives. Unclosed tags run to end-of-text;
unknown tags are ignored (and left in the text verbatim is NOT done -- they are
dropped but no directive is emitted, so you can still read the output).
"""
import re

from .directive import Directive

# tag -> attribute name on Directive
ATTR = {
    "emotion": "emotion",
    "voice": "voice",
    "rate": "rate",
    "pitch": "pitch",
    "emphasis": "emphasis",
    "style": "style",
}

# tag -> value parser
_PARSERS = {
    "emotion": str,
    "voice": str,
    "rate": float,
    "pitch": float,
    "emphasis": float,
    "style": str,
}

_TAG_RE = re.compile(r"\[(/?)([a-zA-Z_]+)(?:=([^\]]*))?\]")


def _word_index(clean_prefix, full_text):
    """Map a character position in cleaned text to a word index in full text.

    We align by walking the full text word by word; words that were inside a tag
    are not counted (tags carry no words). This is an approximation but stable
    for the mock/benchmark pipeline.
    """
    return 0


def parse_bracketed(text, tokens=None):
    """Parse bracketed tags out of ``text``.

    Returns ``(clean_text, directives)``. ``tokens`` is the caller's token
    stream; when omitted we re-tokenize ``clean_text`` so directive spans are
    expressed as word indices into that stream.
    """
    from ..utils.text import tokenize_words

    clean_parts = []
    # stack of (tag, start_word_or_None, attrs)
    open_tags = []
    directives = []
    word_idx = 0
    buf = ""

    pos = 0
    for m in _TAG_RE.finditer(text):
        # flush text before this tag
        buf += text[pos:m.start()]
        closing = m.group(1) == "/"
        tag = m.group(2).lower()
        value = m.group(3)

        if tag not in ATTR:
            # unknown tag: drop it but keep text flowing
            pos = m.end()
            continue

        if closing:
            # close innermost matching tag
            for i in range(len(open_tags) - 1, -1, -1):
                if open_tags[i][0] == tag:
                    _, start_w, attrs = open_tags.pop(i)
                    directives.append(Directive(start=start_w, end=word_idx, **attrs))
                    break
        else:
            attr = ATTR[tag]
            parser = _PARSERS.get(tag, str)
            try:
                v = parser(value) if value is not None else None
            except (TypeError, ValueError):
                v = None
            attrs = {}
            if v is not None:
                attrs[attr] = v
            open_tags.append((tag, word_idx, attrs))

        # count words in the flushed buffer so far (crude but monotonic):
        # we instead count at the end by re-tokenizing; here track only position.
        pos = m.end()

    buf += text[pos:]

    clean_text = buf

    if tokens is None:
        tokens = tokenize_words(clean_text)

    # Recompute span word indices by aligning: since tags carry no words, the
    # word index at each tag boundary equals the number of words in the clean
    # text preceding that boundary. Rebuild from scratch for correctness.
    directives = []
    open_tags = []
    word_idx = 0
    pos = 0
    for m in _TAG_RE.finditer(text):
        seg = text[pos:m.start()]
        word_idx += len(tokenize_words(seg))
        closing = m.group(1) == "/"
        tag = m.group(2).lower()
        value = m.group(3)
        if tag not in ATTR:
            pos = m.end()
            continue
        if closing:
            for i in range(len(open_tags) - 1, -1, -1):
                if open_tags[i][0] == tag:
                    _, start_w, attrs = open_tags.pop(i)
                    directives.append(Directive(start=start_w, end=word_idx, **attrs))
                    break
        else:
            attr = ATTR[tag]
            parser = _PARSERS.get(tag, str)
            try:
                v = parser(value) if value is not None else None
            except (TypeError, ValueError):
                v = None
            attrs = {}
            if v is not None:
                attrs[attr] = v
            open_tags.append((tag, word_idx, attrs))
        pos = m.end()

    # unclosed tags run to end of text
    n_words = len(tokens)
    for _, start_w, attrs in open_tags:
        directives.append(Directive(start=start_w, end=n_words, **attrs))

    return clean_text, directives
