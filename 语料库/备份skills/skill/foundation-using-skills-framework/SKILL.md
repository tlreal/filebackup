---
name: foundation-using-skills-framework
description: 在开始任何对话时使用 - 确定如何查找和使用 Skills，要求在任何响应前先检查是否有适用的 Skill
---

# Using Skills Framework - 使用 Skills 框架

## 概述

如果你认为有哪怕 1% 的可能某个 skill 适用于你正在做的事情，你**必须**调用那个 skill。

**这不是可选的。这不是可以协商的。你不能用理由逃避这个。**

## 规则

**在任何响应或行动之前调用相关或请求的 skills。**

即使只有 1% 的可能某个 skill 适用，也应该调用它检查。如果调用的 skill 最终对情况不适用，你不需要使用它。

```
收到用户消息
    ↓
有任何 skill 可能适用？
    ↓ 是，哪怕 1%
调用 Skill
    ↓
宣布："使用 [skill] 来 [目的]"
    ↓
有检查清单？
    ↓ 是
为每个项目创建待办事项
    ↓
严格遵循 skill
    ↓
响应（包括澄清）
```

## 红线

这些想法意味着停止——你在找借口：

| 想法 | 现实 |
|------|------|
| "这只是个简单问题" | 问题也是任务。检查 skills。 |
| "我需要先获取更多上下文" | Skill 检查在澄清问题之前。 |
| "让我先探索代码库" | Skills 告诉你如何探索。先检查。 |
| "我可以快速检查 git/文件" | 文件缺少对话上下文。检查 skills。 |
| "让我先收集信息" | Skills 告诉你如何收集信息。 |
| "这不需要正式的 skill" | 如果 skill 存在，就使用它。 |
| "我记得这个 skill" | Skills 会演变。读当前版本。 |
| "这不算任务" | 行动 = 任务。检查 skills。 |
| "Skill 太大材小用" | 简单的事情会变复杂。使用它。 |
| "我先做这一件事" | 做任何事之前先检查。 |

## Skill 优先级

当多个 skills 可能适用时，使用此顺序：

1. **过程 skills 优先**（core-brainstorming, core-systematic-debugging）- 这些决定如何处理任务
2. **实现 skills 其次**（embedded-driver-development, embedded-firmware-build）- 这些指导执行

"让我们构建 X" → 先 core-brainstorming，然后实现 skills。
"修复这个 bug" → 先 core-systematic-debugging，然后领域特定 skills。

## Skill 类型

**严格型**（TDD, debugging）：严格遵循。不要为了方便而调整。

**灵活型**（patterns）：根据上下文调整原则。

Skill 本身会告诉你是哪种。

## 用户指令

指令说的是做什么，不是如何做。"添加 X" 或 "修复 Y" 不意味着跳过工作流。

## 与 Core Workflow 的关系

这个 Skill 是整个框架的入口点：

1. **Think 阶段** → 使用 `core-brainstorming`
2. **Plan 阶段** → 使用 `core-writing-plans`, `core-test-driven-development`
3. **Act 阶段** → 使用 `core-executing-plans`, `core-subagent-driven-development` 等

同时根据项目类型激活领域扩展：
- 嵌入式项目 → `embedded-*`
- 仿真项目 → `simulation-*`
