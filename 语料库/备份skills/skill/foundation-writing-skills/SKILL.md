---
name: foundation-writing-skills
description: 在创建新 Skills、编辑现有 Skills 或验证 Skills 有效时使用
---

# Writing Skills - 编写 Skills

## 概述

**编写 Skills 就是将 TDD（测试驱动开发）应用于流程文档。**

你编写测试用例（压力场景），观察它失败（基线行为），编写 skill（文档），观察测试通过（AI 遵守），然后重构（堵住漏洞）。

**核心原则:** 如果你没有看到 AI 在没有 skill 的情况下失败，你不知道 skill 是否教对了。

## 什么是 Skill？

**Skill** 是经过验证的技术、模式或工具的参考指南。Skills 帮助未来的 AI 实例找到并应用有效的方法。

**Skills 是：** 可复用的技术、模式、工具、参考指南

**Skills 不是：** 关于你如何解决一次问题的叙述

## Skill 类型

### 技术类（Technique）
具体的方法和步骤（condition-based-waiting, root-cause-tracing）

### 模式类（Pattern）
思考问题的方式（flatten-with-flags, test-invariants）

### 参考类（Reference）
API 文档、语法指南、工具文档

## 目录结构

```
skills/
  skill-name/
    SKILL.md              # 主参考（必需）
    supporting-file.*     # 仅在需要时
```

**扁平命名空间** - 所有 skills 在一个可搜索的命名空间中

**单独文件用于：**
1. **重型参考**（100+ 行）- API 文档、综合语法
2. **可复用工具** - 脚本、工具、模板

**保持内联：**
- 原则和概念
- 代码模式（< 50 行）
- 其他所有

## SKILL.md 结构

**Frontmatter (YAML):**
- 只有两个字段：`name` 和 `description`
- 最大 1024 字符
- `name`: 只用字母、数字和连字符
- `description`: 第三人称，只描述何时使用（不是做什么）

```markdown
---
name: skill-name-with-hyphens
description: Use when [具体触发条件和症状]
---

# Skill Name

## 概述
这是什么？1-2 句核心原则。

## 何时使用
[小型内联流程图，如果决策不明显]

使用场景列表
何时不使用

## 核心模式（用于技术/模式）
前后代码对比

## 快速参考
扫描常见操作的表格或要点

## 实现
简单模式的内联代码
重型参考或可复用工具链接到文件

## 常见错误
什么会出错 + 修复

## 真实影响（可选）
具体结果
```

## 描述字段的重要性

**关键：描述 = 何时使用，不是 Skill 做什么**

描述应该只描述触发条件。不要在描述中总结 skill 的流程或工作流。

**为什么重要：** 测试表明，当描述总结了 skill 的工作流时，AI 可能遵循描述而不是阅读完整的 skill 内容。

```yaml
# ❌ 错误：总结工作流
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ✅ 正确：只有触发条件
description: Use when executing implementation plans with independent tasks
```

## 何时创建 Skill

**创建当：**
- 技术对你来说不是直观明显的
- 你会跨项目引用这个
- 模式广泛适用（不是项目特定的）
- 其他人会受益

**不创建用于：**
- 一次性解决方案
- 其他地方有良好文档的标准实践
- 项目特定约定（放在 CLAUDE.md）

## 红绿重构循环

| TDD 概念 | Skill 创建 |
|----------|-----------|
| **测试用例** | 带 AI 的压力场景 |
| **生产代码** | Skill 文档 (SKILL.md) |
| **测试失败 (RED)** | AI 没有 skill 时违反规则 |
| **测试通过 (GREEN)** | 有 skill 时 AI 遵守 |
| **重构** | 堵住漏洞同时保持遵守 |
