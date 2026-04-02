---
name: core-finishing-branch
description: 当所有任务完成后使用，完成开发分支的收尾工作
---

# Finishing Branch - 完成开发分支

## 概述

当实施计划的所有任务完成后，进行分支收尾工作。

## 流程

### 1. 验证完成状态

- 所有任务已标记完成
- 所有测试通过
- 没有未解决的审查问题

### 2. 最终检查

```bash
# 运行完整测试套件
npm test  # 或对应的测试命令

# 检查代码质量
npm run lint

# 确认没有未提交的更改
git status
```

### 3. 提供选项

向用户提供以下选项：

1. **合并到主分支**
   ```bash
   git checkout main
   git merge --no-ff feature-branch
   git push
   ```

2. **创建 Pull Request**
   - 推送分支
   - 创建 PR 描述
   - 等待审查

3. **保留分支**
   - 暂不合并
   - 记录分支状态

4. **放弃分支**
   ```bash
   git checkout main
   git branch -D feature-branch
   ```

### 4. 清理

如果使用了 git worktree：
```bash
git worktree remove ../worktree-path
```

## 输出模板

```markdown
## 开发分支完成报告

### 完成状态
- ✅ 所有任务: 已完成
- ✅ 测试: 全部通过
- ✅ 审查: 已批准

### 选项
请选择如何处理此分支：

1. 合并到 main
2. 创建 Pull Request
3. 保留分支（稍后处理）
4. 放弃分支

您的选择是？
```
