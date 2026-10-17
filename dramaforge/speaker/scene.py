"""Multi-speaker scene planning: assign voices to spans, plan hand-offs.

A "scene" is a sequence of speaker turns. The planner turns word-level voice
attributes into speaker turns and inserts cross-fades at boundaries so a hard
speaker switch becomes a clean hand-off.
"""
from dataclasses import dataclass, field


@dataclass
class SpeakerTurn:
    speaker: str
    start_word: int
    end_word: int
    crossfade_ms: float = 30.0


def plan_turns(words, attrs, default_voice, crossfade_ms=30.0):
    """Group consecutive words with the same voice into turns.

    Returns a list of ``SpeakerTurn``. Words whose voice is empty inherit
    ``default_voice``.
    """
    turns = []
    cur = None
    for i, (w, a) in enumerate(zip(words, attrs)):
        voice = a.voice or default_voice
        if cur is None or cur.speaker != voice:
            cur = SpeakerTurn(speaker=voice, start_word=i, end_word=i + 1,
                              crossfade_ms=crossfade_ms)
            turns.append(cur)
        else:
            cur.end_word = i + 1
    return turns
