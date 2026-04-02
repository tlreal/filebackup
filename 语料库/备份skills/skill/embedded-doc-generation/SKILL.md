---
name: embedded-doc-generation
description: 生成项目文档，包括 API 文档、用户手册等
workflow_phase: act
domain: embedded
---

# Doc Generation - 文档生成

## 概述

为嵌入式项目生成各类文档，包括 API 文档、设计文档和用户手册。

## 文档类型

### 1. API 文档

使用 Doxygen 生成：

```c
/**
 * @brief 初始化驱动
 * @param config 配置结构体指针
 * @return 0 成功，-1 失败
 */
int drv_init(const drv_config_t *config);
```

```bash
# 生成配置
doxygen -g Doxyfile

# 生成文档
doxygen Doxyfile
```

### 2. 设计文档

模板结构：
```markdown
# [模块名称] 设计文档

## 1. 概述
## 2. 架构设计
## 3. 接口定义
## 4. 数据结构
## 5. 流程说明
## 6. 注意事项
```

### 3. 用户手册

包含内容：
- 快速开始
- 安装配置
- 功能说明
- 常见问题

## 文档规范

| 规范 | 说明 |
|------|------|
| 语言 | 中英文并重 |
| 格式 | Markdown 为主 |
| 图表 | 使用 Mermaid |
| 版本 | 与代码同步 |

## 输出清单

- [ ] API 参考文档
- [ ] 设计说明文档
- [ ] 用户使用手册
- [ ] 版本更新日志

## 与 Core Workflow 集成

**在 Act 阶段调用:**
- 代码实现完成后
- 准备发布前
