# 流式合成

`configs/streaming.yaml` 用更小的帧率、更轻的码本，换取更低的首包延迟。

## 关键参数

- `prosody.frame_rate`：每秒韵律帧数，越小延迟越低、越省算力
- `codec.n_quantizers`：量化级数，少则 token 少、编码快
- `acoustic.hop_length` / `vocoder.hop_length`：每帧采样数，决定输出粒度

## 可复用要点

流式 = 分块处理 + 状态复用。真实系统中把「韵律/声学」按句子分块推进、`vocoder` 逐 hop 吐波形，就能边生成边播。本项目 `AudioResult.waveform` 是整段 list，替换成生成器/队列即得流式。
