# 执导语法（Directive Syntax）

执导语音 = 告诉引擎「哪个片段用什么语气、谁来说、说多快」。支持两套等价语法。

## 1. Bracketed tags（精确、可编程）

| Tag | 取值 | 示例 |
|-----|------|------|
| `[emotion=...]` | angry / happy / sad / gentle / excited / fearful / surprised / neutral | `[emotion=angry]滚！[/emotion]` |
| `[voice=...]` | 任意说话人名 | `[voice=alice]你好[/voice]` |
| `[rate=...]` | 浮点倍率（1.0 正常） | `[rate=0.8]慢慢说[/rate]` |
| `[pitch=...]` | 浮点倍率 | `[pitch=1.2]高一点[/pitch]` |
| `[emphasis=...]` | 0.0~1.0 | `[emphasis=0.8]重读[/emphasis]` |
| `[style=...]` | whisper / shout / sing / robot / dramatic | `[style=whisper]悄悄话[/style]` |

标签可嵌套、可跨词；未闭合的标签延续到文末。

## 2. 自然语言执导（对人友好）

```
"用愤怒的语气说第一句，然后换成温柔的语气"
"让爱丽丝说这句话"
"语速快一点，音调高一点"
```

规则关键词映射（零依赖、不调 LLM）：

- 情感：愤怒/生气 → angry，开心 → happy，悲伤 → sad，温柔 → gentle …
- 语速：快/加速 → rate 1.2，慢/减速 → rate 0.85
- 音高：音调高 → pitch 1.15，音调低 → pitch 0.85
- 重读：重读/强调 → emphasis 0.8
- 说话人：`让<名字>说` → voice=<名字>

> 生产落地时，这一层替换成一个小型指令微调模型，输出 `Directive` 的 JSON（见 `prompts/`），引擎不用改。

## 3. 词级控制原理

两种语法最终都变成「区间指令」，`apply_directives` 逐词求交集。因此一句话中间换情绪、换说话人，是天然支持的，无需特殊 API。
