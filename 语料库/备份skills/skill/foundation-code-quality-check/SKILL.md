---
name: foundation-code-quality-check
description: 执行代码质量检查，包括静态分析、规范检查和安全扫描
---

# Code Quality Check - 代码质量检查

## 概述

对代码进行系统性的质量检查，确保符合规范和最佳实践。

## 检查维度

### 1. 静态分析

**C/C++ 代码:**
```bash
# cppcheck
cppcheck --enable=all --error-exitcode=1 src/

# PC-lint (商业)
lint-nt options.lnt src/*.c
```

**Python 代码:**
```bash
# pylint
pylint src/

# flake8
flake8 src/
```

### 2. 代码规范

**格式检查:**
```bash
# clang-format (C/C++)
clang-format --dry-run --Werror src/*.c

# black (Python)
black --check src/
```

**命名规范:**
- 函数：动词开头，小写+下划线
- 变量：名词，表明含义
- 常量：全大写+下划线
- 类型：首字母大写

### 3. 安全检查

**常见问题:**
- 缓冲区溢出风险
- 整数溢出
- 未初始化变量
- 空指针解引用

### 4. 复杂度检查

**圈复杂度限制:**
- 函数 < 15
- 过高表示需要拆分

## 嵌入式特有检查

### 内存安全

- [ ] 没有动态内存分配（或有明确管理）
- [ ] 栈使用在限制内
- [ ] 没有悬空指针

### 中断安全

- [ ] 中断处理函数简短
- [ ] 共享变量正确保护
- [ ] 没有阻塞操作

### 资源管理

- [ ] 外设正确初始化
- [ ] 资源正确释放
- [ ] 没有资源泄漏

## 输出格式

```markdown
## 代码质量报告

### 静态分析
- 错误: 0
- 警告: 3
- 建议: 5

### 规范检查
- 格式问题: 2 files
- 命名问题: 1

### 问题列表
| 文件 | 行号 | 级别 | 描述 |
|------|------|------|------|
| xxx.c | 42 | Warning | Potential buffer overflow |

### 建议
[改进建议列表]
```
