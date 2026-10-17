# 基准说明

5 个基准覆盖「可执导合成」的核心能力面：

| 基准 | 测什么 | 信号来源 |
|------|--------|----------|
| directive_adherence | 执导遵循度 | mock 后端 obedience（skill 驱动） |
| mos | 自然度 MOS | 遵循度线性映射 1~5 |
| speaker_similarity | 说话人可分性 | 确定性嵌入两两 cosine |
| speaker_switch | 多说话人切换 | 对话 turn 切分准确率 |
| rvq_efficiency | 编解码压缩 | 帧→token + 重建 RMSE |

运行：`python -m dramaforge.cli bench --config configs/default.yaml`
