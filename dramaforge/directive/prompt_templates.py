"""Reusable direction-prompt templates (technical handoff).

These are the exact prompt shapes a caller hands to an instruction-tuned model
to get back structured direction JSON -- the output of which feeds
:func:`dramaforge.directive.parser` via its ``Directive`` objects.
"""

DIRECTION_SYSTEM = (
    "You are a speech direction annotator. Given a script and a natural-language "
    "direction, emit JSON: a list of spans with start/end word indices and "
    "attributes {emotion, voice, rate, pitch, emphasis, style}. Only the words "
    "the user changed need a span; omit defaults."
)

DIRECTION_USER = (
    "Script: {script}\n\nDirection: {direction}\n\n"
    "Return JSON: {{\"spans\": [{{\"start\": 0, \"end\": 5, \"emotion\": \"angry\"}}]}}"
)

MOS_RUBRIC = (
    "Rate the synthesized audio 1-5 for: naturalness (human-like), speaker "
    "similarity (does it match the requested voice), and directive adherence "
    "(did it follow tone/emotion/pace instructions). Report three numbers."
)
