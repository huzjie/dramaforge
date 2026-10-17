# dramaforge 架构

## 一句话定位

把「自然语言执导 + 词级音色/情感控制 + 多说话人场景」编译成一段可合成的语音：文本先被解析成**带区间的执导指令**，再逐词解析出属性，最后经「韵律 → 声学 → 编解码 → 声码」两阶段流水线产出波形。

## 数据流

```
text + direction
   │  parse_text()          bracketed tags + 自然语言执导
   ▼
clean_text + Directive[]（区间指令：emotion/voice/rate/pitch/emphasis/style）
   │  apply_directives()
   ▼
WordAttributes[]（每个词独立属性 = 词级控制）
   │  plan_turns()
   ▼
SpeakerTurn[]（说话人分段 + 交叉淡入淡出）
   │  backend.synthesize()
   ▼
Prosody → Emotion → Acoustic → RVQ Codec → Vocoder
   │
   ▼
AudioResult{waveform, codes, metadata}
```

## 关键设计决策

1. **执导统一成一种表示**：bracketed tags 和自然语言执导都产 `Directive`，引擎只认这一种结构。这样「换一个指令解析器」或「接一个指令微调模型」都不动引擎。

2. **词级 = 区间覆盖**：`apply_directives` 用 `[start, end)` 半开区间覆盖词索引，重叠时后写的赢。词级控制不是新数据结构，而是「区间解析」的自然结果。

3. **说话人切换用交叉淡入**：`plan_turns` 把相邻词按 voice 分组，turn 边界用 `crossfade` 平滑，避免硬切爆音。

4. **零依赖但分两阶段**：声学模型产出 mel 帧，声码器把 mel 变波形，中间夹一个 RVQ 编解码——这是「音频即 token 序列」的现代编解码思路。

## 目录

- `directive/` 执导解析（tags + 自然语言）
- `speaker/` 说话人嵌入与库
- `codec/` RVQ 残差向量量化
- `prosody/` 韵律预测（音高/能量/时长）
- `emotion/` 情感嵌入
- `acoustic/` 声学模型（文本→mel）
- `vocoder/` 声码器（mel→波形）
- `engine/` 编排 + 音频工具
- `backends/` mock/cpu 后端 + 注册
- `train/` 可训练 skill
- `bench/` MOS / 相似度 / 执导一致性 / 切换 / RVQ
