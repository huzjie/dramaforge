# 集成

- **LangChain**：`integrations/langchain.py` 的 `build_dramaforge_tool(engine)` 把引擎包成 tool
- **MCP**：`integrations/mcp.py` 的 `mcp_tool_schema()` 提供 tool 定义
- **任意 TTS 后端**：在 `backends/` 注册新后端，实现 `synthesize(...)` 返回 `AudioResult`
