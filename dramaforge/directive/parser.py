"""Natural-language direction parser (zero-dependency, keyword driven).

The prompt-style direction ("say the first sentence angrily, then switch to a
warm tone") is turned into the same ``Directive`` objects the tag parser emits,
so the engine only ever sees one representation.

The parser is intentionally small and rule-based: it scans for
``attribute := value`` phrases. It is NOT an LLM call -- it is the *layer that
feeds an LLM's output* (or a human prompt) into the synthesis engine. In a real
stack this is exactly where a small instruction-tuned model would sit.
"""
from .directive import Directive

# emotion keywords -> canonical emotion
EMOTIONS = {
    "愤怒": "angry", "生气": "angry", "怒": "angry", "angry": "angry",
    "开心": "happy", "高兴": "happy", "快乐": "happy", "happy": "happy",
    "悲伤": "sad", "难过": "sad", "sad": "sad",
    "温柔": "gentle", "柔和": "gentle", "gentle": "gentle",
    "兴奋": "excited", "激动": "excited", "excited": "excited",
    "平静": "neutral", "中性": "neutral", "neutral": "neutral",
    "害怕": "fearful", "恐惧": "fearful", "fearful": "fearful",
    "惊喜": "surprised", "惊讶": "surprised", "surprised": "surprised",
}

STYLES = {
    "低语": "whisper", "耳语": "whisper", "whisper": "whisper",
    "大喊": "shout", "吼": "shout", "shout": "shout",
    "唱歌": "sing", "唱": "sing", "sing": "sing",
    "机器人": "robot", "robot": "robot",
    "戏剧": "dramatic", "dramatic": "dramatic",
}


def _find_emotion(seg):
    seg_l = seg.lower()
    for k, v in EMOTIONS.items():
        if k in seg_l:
            return v
    return None


def _find_style(seg):
    seg_l = seg.lower()
    for k, v in STYLES.items():
        if k in seg_l:
            return v
    return None


def parse_natural(text, n_words):
    """Parse plain-language direction into directives covering ``[0, n_words)``.

    Returns a list of ``Directive``. Without explicit spans the whole text is
    assumed; the caller can further split into sentence spans by passing
    ``n_words`` per sentence. This is a demonstration-level heuristic: a real
    deployment swaps this for an instruction-tuned model returning JSON.
    """
    directives = []
    seg_l = text.lower()

    emotion = _find_emotion(text)
    style = _find_style(text)

    rate = 1.0
    pitch = 1.0
    emphasis = 0.0
    voice = ""

    if any(k in seg_l for k in ("快", "加速", "语速快", "faster", "speed up")):
        rate = 1.2
    if any(k in seg_l for k in ("慢", "减速", "语速慢", "slower", "slow down")):
        rate = 0.85
    if any(k in seg_l for k in ("音调高", "高音", "pitch up", "higher pitch")):
        pitch = 1.15
    if any(k in seg_l for k in ("音调低", "低音", "pitch down", "lower pitch")):
        pitch = 0.85
    if any(k in seg_l for k in ("重读", "强调", "加重", "emphasize")):
        emphasis = 0.8

    # voice: "让<名字>说" / "用<名字>的声音"
    import re
    m = re.search(r"(?:让|用)([\u4e00-\u9fa5a-zA-Z]+)(?:说|的声音|的声音说|来讲|来读)", text)
    if m:
        voice = m.group(1).strip()

    directives.append(Directive(
        start=0, end=n_words, emotion=emotion or "neutral",
        voice=voice, rate=rate, pitch=pitch, emphasis=emphasis, style=style or "",
    ))
    return directives


def parse_text(text, tokens=None):
    """Parse both bracketed tags and natural-language direction from ``text``.

    Returns ``(clean_text, directives, tokens)``.
    """
    from ..utils.text import tokenize_words
    from .tags import parse_bracketed

    clean_text, directives = parse_bracketed(text, tokens=None)
    tokens = tokenize_words(clean_text)
    return clean_text, directives, tokens
