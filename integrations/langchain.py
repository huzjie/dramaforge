"""LangChain integration: expose dramaforge as a text->speech tool.

Requires the optional ``langchain`` package. Kept separate so the core package
stays zero-dependency.
"""


def build_dramaforge_tool(engine):
    """Return a callable compatible with LangChain tool schemas.

    The tool takes a JSON string ``{"text": ..., "emotion": ..., "voice": ...,
    "direction": ...}`` and returns the audio metadata as a string.
    """
    import json

    def dramaforge_tool(input_json: str) -> str:
        payload = json.loads(input_json)
        r = engine.synth(payload.get("text", ""),
                         direction=payload.get("direction"),
                         voice=payload.get("voice"),
                         emotion=payload.get("emotion"))
        return json.dumps(r.as_dict(), ensure_ascii=False)

    return dramaforge_tool
