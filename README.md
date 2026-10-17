# dramaforge

**可执导多说话人语音合成引擎** — 词级音色/情感/语速控制 + 多说话人场景 + 自然语言执导，零依赖纯 Python 参考实现（对标 Fish Audio Drama 3 的可执导 TTS 方向）。

[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![zero-deps](https://img.shields.io/badge/deps-zero-brightgreen.svg)](pyproject.toml)

---

## 这个引擎解决什么问题

传统 TTS 是「文字进、固定音色出」。可执导 TTS 要的是：**一段文本里，第 3 个词用愤怒的语气重读、第 5 个词换成另一个人的声音、这一句整体放慢** —— 导演怎么跟配音演员说，你就怎么跟模型说。

`dramaforge` 把这个能力拆成一条可复用的流水线，全部纯 Python、零依赖、可运行、可训练、可基准评测。

## 技术原理（怎么实现）

### 1. 执导统一成一种表示：区间指令 `Directive`

不管是 `[emotion=angry]...[/emotion]` 这种精确标签，还是「用愤怒的语气说第一句」这种自然语言，解析后都变成同一种结构：

```python
Directive(start=0, end=5, emotion="angry", voice="", rate=1.0, pitch=1.0, emphasis=0.0)
```

`start/end` 是**词下标区间**（半开 `[start, end)`）。引擎只认这一种结构，所以「换一个执导解析器」或「接一个指令微调模型」都不动引擎——这是把「控制」与「合成」解耦的关键。

### 2. 词级控制 = 区间覆盖，不是新数据结构

`apply_directives()` 逐词求「覆盖该词的指令交集」，重叠时后写的赢。于是「一句话中间换情绪、换说话人」是区间解析的自然结果，无需任何特殊 API：

```python
attrs = apply_directives(words, directives, defaults)
# attrs[0].emotion == "angry"   （被 [emotion=angry] 覆盖）
# attrs[2].emotion == "neutral" （未被覆盖，回退默认）
```

### 3. 说话人切换用交叉淡入，避免硬切爆音

`plan_turns()` 把相邻同 voice 的词归组，turn 边界用 `crossfade(ms)` 做短交叉淡化，而不是直接把两段波形拼一起。这是多说话人合成里最容易踩的坑——硬切会产生 click 爆音。

### 4. RVQ 残差向量量化：音频即 token 序列

现代神经音频编解码（SoundStream / EnCodec / Drama 系）把音频表示成**多级离散码**。第 1 个码本抓粗形状，后续码本量化**残差**，解码时逐级相加。`dramaforge/codec/rvq.py` 是纯 Python 参考实现：`token_count = n_frames × n_quantizers`，重建误差随量化器数量单调下降。

### 5. 两阶段合成：韵律 → 声学 → 编解码 → 声码

```
Prosody(音高/能量/时长) → Acoustic(文本→mel帧) → RVQ Codec(离散码) → Vocoder(mel→波形)
```

每一层都是独立可替换的模块——想换更好的韵律模型或声码器，只改那一层。

## 快速开始

```bash
git clone https://github.com/huzjie/dramaforge
cd dramaforge
python -m dramaforge.doctor          # 自检：跑通全部组件 + 合成冒烟
python -m dramaforge.cli bench       # 跑基准
```

Python API：

```python
from dramaforge import Config, DramaEngine

engine = DramaEngine(Config())
r = engine.synth(
    "[emotion=angry]我真的受够了！[/emotion] 然后她[rate=0.8]慢慢地说[/rate]",
    direction="最后换成温柔的语气",
)
print(r.as_dict())                    # 时长 / 词属性 / 说话人分段 / RVQ 码
from dramaforge.engine.audio import save_wav
save_wav("out.wav", r.waveform, r.sample_rate)
```

HTTP 服务：

```bash
python -m dramaforge.cli serve --config configs/default.yaml
curl -X POST http://127.0.0.1:8000/v1/audio/speech \
     -H 'Content-Type: application/json' \
     -d '{"text": "你好世界", "emotion": "gentle", "voice": "alice"}'
```

## 执导语法

**Bracketed tags（精确）**：`[emotion=angry]` `[voice=alice]` `[rate=0.8]` `[pitch=1.2]` `[emphasis=0.8]` `[style=whisper]`，成对闭合，可嵌套跨词。

**自然语言执导（友好）**：「用愤怒的语气」「让爱丽丝说」「语速快一点」「重读这个词」——规则关键词映射（零依赖、不调 LLM），生产时可换成指令微调模型输出 `Directive` JSON。

详见 [docs/directive_syntax.md](docs/directive_syntax.md)。

## 可复用要点（干货块）

1. **控制与合成解耦**：执导永远先编译成「区间指令」，再喂给合成器。换解析器、换模型、换后端，都不动核心引擎。
2. **残差量化是「多级近似」通用套路**：不限于音频，图像 VQ / 动作 VQ 同理。判断级数够不够看重建误差收敛曲线，别拍脑袋。
3. **说话人切换必须淡入淡出**：多说话人、多音色拼接统一走 crossfade，硬切会爆音。
4. **训练信号要「单调趋 1」**：mock 后端用 `boost=(skill-0.5)*2`，skill=0.5 时命中率恰为随机 0.5、skill=1.0 恒遵守，曲线干净可验证（详见 `train/`）。
5. **音频即 token**：把波形压成离散码序列，语音生成就能被语言模型当文本一样自回归，统一建模。

## 基准

真实测量（`python -m dramaforge.cli bench --config configs/default.yaml`）：

| 基准 | skill=0.5（基线） | skill=1.0（训练后） | 说明 |
|------|-------------------|---------------------|------|
| directive_adherence | 0.25 | 1.00 | 执导遵循度（mock 后端随 skill 单调趋 1） |
| mos | 3.0 | 5.0 | 自然度 MOS（由遵循度线性映射 1~5） |
| speaker_similarity | self 1.00 / cross 0.012 | 同左 | 自相似 1.0，两两余弦 0.012（正交可分） |
| speaker_switch | 3/3（准确率 1.0） | 同左 | 三说话人对话 turn 切分全对 |
| rvq_efficiency | 40 帧→160 token（4/帧），rmse 0.592 | 同左 | 帧→token 压缩 + 重建误差 |

## 目录

```
dramaforge/
  directive/   执导解析（tags + 自然语言）
  speaker/     说话人嵌入与库
  codec/       RVQ 残差向量量化
  prosody/     韵律预测
  emotion/     情感嵌入
  acoustic/    声学模型（文本→mel）
  vocoder/     声码器（mel→波形）
  engine/      编排 + 音频工具
  backends/    mock/cpu 后端
  train/       可训练 skill
  bench/       基准
  serving/     stdlib HTTP
docs/          架构 / 执导语法 / 编解码 / 提示词模板
prompts/       执导提示词模板
recipes/       有声书 / 播客 / 对话 / 广告 配方
examples/      可运行示例
deploy/        Docker / K8s / Helm / CI
```

## License

Apache-2.0，详见 [LICENSE](LICENSE)。
