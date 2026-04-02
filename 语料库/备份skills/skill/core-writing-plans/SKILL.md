---
name: core-writing-plans
description: 当有规格或需求用于多步骤任务时使用，在开始写代码之前
---

# Writing Plans - 编写实施计划

## 概述

编写全面的实施计划，假设执行者对代码库零了解且判断力有限。记录他们需要知道的一切：每个任务要修改哪些文件、代码、测试、需要检查的文档、如何测试。将完整计划拆解成小任务。DRY. YAGNI. TDD. 频繁提交。

假设执行者是熟练的开发者，但对我们的工具集或问题领域几乎不了解。假设他们不太擅长测试设计。

**开始时宣布:** 「我正在使用 writing-plans 技能来创建实施计划。」

**保存计划到:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 任务粒度

**每一步是一个动作（2-5分钟）：**
- 「编写失败的测试」 - 一步
- 「运行确认测试失败」 - 一步  
- 「实现最小代码使测试通过」 - 一步
- 「运行测试确认通过」 - 一步
- 「提交」 - 一步

## 计划文档头部

**每个计划必须以此头部开始：**

```markdown
# [功能名称] 实施计划

> **For Claude:** REQUIRED SUB-SKILL: 使用 core-executing-plans 逐任务实施此计划。

**目标:** [一句话描述要构建什么]

**架构:** [2-3句话关于方案]

**技术栈:** [关键技术/库]

---
```

## 任务结构

```markdown
### 任务 N: [组件名称]

**文件:**
- 创建: `exact/path/to/file.py`
- 修改: `exact/path/to/existing.py:123-145`
- 测试: `tests/exact/path/to/test.py`

**步骤 1: 编写失败的测试**

[具体测试代码]

**步骤 2: 运行测试验证失败**

运行: `pytest tests/path/test.py::test_name -v`
期望: FAIL，提示 "function not defined"

**步骤 3: 编写最小实现**

[具体实现代码]

**步骤 4: 运行测试验证通过**

运行: `pytest tests/path/test.py::test_name -v`
期望: PASS

**步骤 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 领域扩展钩子

**如果是嵌入式项目，计划应包含：**
- **RECOMMENDED:** 考虑内存布局 - 使用 `embedded-memory-optimization`
- **RECOMMENDED:** 考虑功耗模式 - 使用 `embedded-power-optimization`
- **RECOMMENDED:** 考虑硬件接口时序

## 记住

- 始终使用精确文件路径
- 计划中包含完整代码（不是「添加验证」）
- 精确命令和预期输出
- 使用 @ 语法引用相关 skills
- DRY, YAGNI, TDD, 频繁提交

## 执行交接

保存计划后，提供执行选择：

**「计划已完成并保存到 `docs/plans/<filename>.md`。两种执行方式：**

**1. 子代理驱动（当前会话）** - 每个任务派发新鲜子代理，任务间审查，快速迭代

**2. 并行会话（独立）** - 打开新会话使用 executing-plans，批量执行带检查点

**选择哪种方式？」**

**如果选择子代理驱动：**
- **REQUIRED SUB-SKILL:** 使用 `core-subagent-driven-development`

**如果选择并行会话：**
- **REQUIRED SUB-SKILL:** 新会话使用 `core-executing-plans`
