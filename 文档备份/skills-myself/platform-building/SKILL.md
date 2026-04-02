---
name: platform-building
description: 从零开始构建 Web 应用平台原型 - 需求分析、架构设计、实施计划、代码实现、测试验证全流程
---

# Platform Building - Web 平台构建

## 概述

指导 AI 快速构建 Web 应用平台原型，形成"AI + Skills 驱动平台构建"流程闭环。

**适用场景**:
- 前后端分离的 Web 应用
- 数据上报/监管类平台
- RESTful API + WebSocket 实时通信
- CRUD 管理后台

**开始时宣布:** 「我正在使用 platform-building 技能来构建 Web 平台。」

---

## 流程闭环

```
需求分析 → 架构设计 → 实施计划 → 代码实现 → 测试验证 → 知识沉淀
core-      embedded-  core-      core-      core-       [沉淀回Skill]
brainstorming  architecture  writing  executing  verification
              -design    -plans    -plans
```

---

## 阶段 1: 需求分析 (使用 core-brainstorming)

**目标**: 通过协作对话明确平台需求

**步骤**:

1. **了解项目上下文**
   - 读取现有项目文档（如有）
   - 了解业务背景和目标用户
   - 确认与现有系统的关系

2. **逐项确认需求决策**（一次一个问题）

| 决策项 | 提问示例 |
|--------|----------|
| 部署方式 | 独立项目 vs 同仓库多模块 |
| 技术栈 | Python FastAPI / Node.js / Java |
| 数据库 | PostgreSQL / MySQL / MongoDB / InfluxDB |
| 认证方式 | JWT / OAuth2 / HMAC-SHA256 |
| 实时通信 | 是否需要 WebSocket |
| 前端风格 | 政务蓝白 / 深色主题 / 数据大屏 |

3. **输出需求决策记录**
```
文件: docs/{project-name}-requirements.md

## 需求决策汇总

| 序号 | 决策项 | 决策结果 | 决策依据 |
|------|--------|---------|---------|
| 1 | 部署方式 | 独立项目 | 用户选择 |
| 2 | 技术栈 | Python FastAPI + React | 采纳建议 |
...
```

---

## 阶段 2: 架构设计 (使用 embedded-architecture-design)

**目标**: 设计系统整体架构

**步骤**:

1. **确定架构风格**
   - 分层架构 (Layered)
   - 六边形架构 (Hexagonal)
   - CQRS

2. **系统分解**
   - 表现层 (Presentation)
   - 应用层 (Application)
   - 领域层 (Domain)
   - 基础设施层 (Infrastructure)

3. **接口定义**
   - RESTful API 端点
   - 数据模型 (Schema/DTO)
   - 事件/消息格式

4. **输出设计文档**
```
文件: docs/{project-name}-design.md

## 1. 系统架构
## 2. 技术栈
## 3. 核心模块
## 4. 数据模型
## 5. API 接口
## 6. 部署架构
```

---

## 阶段 3: 实施计划 (使用 core-writing-plans)

**目标**: 将设计转化为可执行的任务清单

**计划文档头部**（必须包含）:
```markdown
# [项目名称] 实施计划

> **For Claude:** REQUIRED SUB-SKILL: 使用 core-executing-plans 逐任务实施此计划。

**目标:** [一句话描述要构建什么]

**架构:** [2-3句话关于方案]

**技术栈:** [关键技术/库]

---
```

**任务粒度**: 每个任务 1-2 小时可完成

**任务模板**:
```markdown
### 任务 N: [任务标题]

**目标**: [一句话描述]

**文件**:
- 创建: `path/to/file.ext`
- 修改: `path/to/file.ext`

**步骤 1**: [子步骤描述]

[代码示例或配置内容]

**验证**: [如何验证任务完成]
```

**保存计划到**: `docs/plans/YYYY-MM-DD-<project-name>-implementation.md`

---

## 阶段 4: 代码实现 (使用 core-executing-plans)

**目标**: 按计划逐步实现功能

**步骤**:

1. **创建项目骨架**
```bash
# 后端
mkdir -p backend/{app/{api/{v1/endpoints},core,schemas,services},tests}

# 前端
npm create vite@latest frontend -- --template react-ts
```

2. **按任务顺序实现**
   - 读取任务描述
   - 创建/修改文件
   - 本地验证
   - 标记完成

3. **代码规范检查**
   - Python: ruff/black
   - TypeScript: eslint/prettier

---

## 阶段 5: 测试验证 (使用 core-verification)

**验证清单**:

```markdown
## 后端验证
- [ ] 服务启动成功 (健康检查返回 200)
- [ ] API 端点可访问
- [ ] 数据库连接正常
- [ ] 单元测试通过

## 前端验证
- [ ] 页面正常渲染
- [ ] API 调用成功
- [ ] WebSocket 连接正常
- [ ] 无控制台错误

## 集成验证
- [ ] 端到端流程打通
- [ ] 数据流转正确
- [ ] 错误处理正常
```

---

## 常见平台类型模板

### 数据上报监管平台

**特征**: 接收第三方数据上报，存储并展示

**标准组件**:
- 批量接收接口 (POST /api/v1/ingest/batch)
- HMAC 签名验证
- 幂等去重机制
- 时序数据库存储
- WebSocket 推送

**标准端口**:
| 服务 | 端口 |
|------|------|
| 后端 API | 8001 |
| 前端开发 | 5174 |

### CRUD 管理后台

**标准组件**:
- RESTful CRUD 接口
- JWT 认证
- RBAC 权限控制
- 关系型数据库

### 实时监控大屏

**标准组件**:
- WebSocket 推送
- 数据聚合统计
- 缓存优化
- 图表组件

---

## 技术栈推荐

| 场景 | 推荐技术 |
|------|---------|
| 快速开发 | Python FastAPI + React + Ant Design |
| 高性能 | Go + Gin + Vue |
| 企业级 | Java Spring Boot + React |

---

## 文件结构模板

### 后端
```
backend/
├── app/
│   ├── api/v1/endpoints/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── requirements.txt
└── .env.example
```

### 前端
```
frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── types/
├── package.json
└── vite.config.ts
```

---

## MVP 验证标准

```markdown
## 功能完整性
- [ ] 核心业务流程可运行
- [ ] 至少一个端到端场景完整

## 代码质量
- [ ] 无明显的代码重复
- [ ] 有基本的错误处理

## 可运行性
- [ ] 一键启动脚本
- [ ] 环境变量配置完整

## 文档
- [ ] README 说明启动步骤
- [ ] API 文档可访问
```

---

## 记住

- 先后端后前端
- 先核心功能后辅助功能
- 每个任务独立可验证
- 频繁提交，小步前进
- DRY, YAGNI 原则

---

## 知识沉淀

每个项目完成后，更新此 Skill 文档：

```markdown
## 版本历史
| 版本 | 日期 | 变更内容 | 来源项目 |
|------|------|---------|---------|
| v1.0 | 2026-02-24 | 初始版本 | 省级监管平台 |
```

可复用模式：
- TTL 缓存模式
- WebSocket 广播模式
- 幂等去重模式
