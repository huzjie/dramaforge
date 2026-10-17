# Contributing

欢迎 PR。核心原则：保持零依赖（stdlib only）、确定性（可复现）、可测试。

提交前请跑：

```bash
python -m compileall -q dramaforge
python -m unittest discover -s tests -t .
python -m dramaforge.doctor
python -m dramaforge.cli bench --config configs/default.yaml
```
