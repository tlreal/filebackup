---
name: core-using-git-worktrees
description: 在开始需要隔离的功能开发时使用，或在执行实施计划前 - 创建隔离的 git worktree
---

# Using Git Worktrees - 使用 Git Worktrees

## 概述

Git worktrees 创建共享同一仓库的隔离工作区，允许同时在多个分支上工作而无需切换。

**核心原则:** 系统性目录选择 + 安全验证 = 可靠的隔离

**开始时宣布:** "我正在使用 using-git-worktrees skill 来设置隔离工作区。"

## 目录选择流程

按优先级顺序：

### 1. 检查现有目录

```bash
# 按优先级检查
ls -d .worktrees 2>/dev/null     # 首选（隐藏）
ls -d worktrees 2>/dev/null      # 替代
```

**如果找到:** 使用该目录。如果都存在，`.worktrees` 优先。

### 2. 检查 CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**如果指定了偏好:** 直接使用，不询问。

### 3. 询问用户

如果没有目录存在且没有 CLAUDE.md 偏好：

```
未找到 worktree 目录。我应该在哪里创建 worktrees？

1. .worktrees/（项目本地，隐藏）
2. ~/.config/superpowers/worktrees/<项目名>/（全局位置）

您偏好哪个？
```

## 安全验证

### 对于项目本地目录

**创建 worktree 前必须验证目录被忽略：**

```bash
# 检查目录是否被忽略
git check-ignore -q .worktrees 2>/dev/null
```

**如果未被忽略：**
1. 添加到 .gitignore
2. 提交更改
3. 继续创建 worktree

**为什么重要:** 防止意外将 worktree 内容提交到仓库。

## 创建步骤

### 1. 检测项目名

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建 Worktree

```bash
# 创建带新分支的 worktree
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目设置

自动检测并运行适当的设置：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 验证干净基线

运行测试确保 worktree 从干净状态开始：

```bash
npm test  # 或项目适当的命令
```

**如果测试失败:** 报告失败，询问是否继续或调查。

### 5. 报告位置

```
Worktree 已在 <完整路径> 准备好
测试通过（N 个测试，0 失败）
准备实现 <功能名称>
```

## 快速参考

| 情况 | 操作 |
|------|------|
| `.worktrees/` 存在 | 使用它（验证已忽略） |
| `worktrees/` 存在 | 使用它（验证已忽略） |
| 都存在 | 使用 `.worktrees/` |
| 都不存在 | 检查 CLAUDE.md → 询问用户 |
| 目录未被忽略 | 添加到 .gitignore + 提交 |
| 基线测试失败 | 报告失败 + 询问 |

## 与其他 Skills 集成

**被以下调用:**
- **core-brainstorming**（阶段 4）- 设计批准后实现时必需
- 任何需要隔离工作区的 skill

**配合使用:**
- **core-finishing-branch** - 工作完成后清理时必需
- **core-executing-plans** 或 **core-subagent-driven-development** - 工作在此 worktree 中进行
