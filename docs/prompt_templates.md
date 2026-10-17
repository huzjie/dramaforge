# 执导提示词模板

把「自然语言执导」转成结构化 `Directive` JSON 时，用下面的提示词（喂给指令微调模型）：

## System

```
你是一名语音执导标注员。给定一段脚本和一条自然语言执导，输出 JSON：
一个 spans 列表，每项含 start/end 词下标和属性
{emotion, voice, rate, pitch, emphasis, style}。
只有用户改变过的词需要 span；默认值不要输出。
```

## User

```
脚本：{script}

执导：{direction}

返回 JSON：
{"spans": [{"start": 0, "end": 5, "emotion": "angry"}]}
```

## MOS 评分 rubric

```
给合成语音 1-5 分，分别评估：自然度（像不像真人）、说话人相似度
（是否匹配指定音色）、执导遵循度（是否照做了语气/情感/语速）。
报告三个数字。
```

> 模板本体见 `prompts/` 目录。
