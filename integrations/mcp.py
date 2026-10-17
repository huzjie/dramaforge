"""MCP (Model Context Protocol) tool wrapper for dramaforge.

Exposes ``dramaforge_synth`` as an MCP tool definition (schema only; bind to a
real MCP server transport when needed).
"""


def mcp_tool_schema():
    return {
        "name": "dramaforge_synth",
        "description": "Synthesize directable multi-speaker speech.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "emotion": {"type": "string"},
                "voice": {"type": "string"},
                "direction": {"type": "string"},
            },
            "required": ["text"],
        },
    }
