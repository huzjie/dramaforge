# API — backends

- `register_backend(name)` — 装饰器
- `get_backend(name, config)` — 实例化后端
- `list_backends()` — 可用后端
- `MockBackend` — 可训练、确定性；`.skill` / `.obedience(key)` / `.synthesize(...)`
- `CpuBackend` — skill 恒 1.0 的参考实现
