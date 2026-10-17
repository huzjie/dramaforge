# FAQ

**Q: 真的零依赖吗？**
A: 核心包只用 stdlib（`hashlib` / `random` / `math` / `wave` / `struct` / `http.server`）。`integrations/` 里的 LangChain / MCP 是可选、不 import 到核心。

**Q: 能生成真人级语音吗？**
A: 不能。这是「机制参考实现」：执导解析、区间控制、多说话人调度、RVQ 编解码、两阶段流水线都是真实可运行的；声学/声码器是确定性参考（正弦+噪声），换真实模型即可，接口不变。

**Q: skill 是什么？**
A: mock 后端里一个 0~1 的标量，建模「遵循执导指令的程度」，用于演示「训练让执导遵循度提升」这个信号是良定义的。

**Q: 怎么接真实 TTS？**
A: 在 `backends/` 注册新后端，实现 `synthesize(...)` 返回 `AudioResult` 即可，引擎/执导/基准全复用。
