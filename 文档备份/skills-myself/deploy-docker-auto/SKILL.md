---
name: deploy-docker-auto
description: 用于在需要将 TPAIP 项目新版本自动化部署到 Linux 服务器时使用，覆盖镜像构建、远程部署和服务健康检查的完整流程。
---

# Docker 自动部署 - TPAIP 项目

## Overview

自动化部署 TPAIP 项目到 Linux 服务器（192.168.62.38），覆盖代码更新、Docker 镜像构建、打包传输、服务启停和健康检查的完整流程。

## When to Use

- TPAIP 项目需要发布新版本到 192.168.62.38 服务器时
- 需要从 GitLab 拉取最新代码并构建 Docker 镜像进行部署时
- 需要升级 TPAIP 服务版本（如从 2.2.3 升级到 2.2.4）时

## When NOT to Use

- 首次部署 TPAIP 项目（需先手动完成服务器环境初始化：Docker 安装、网络配置等）
- 需要回滚到旧版本时（本 Skill 不包含自动回滚功能，需手动切回旧版本目录）
- 目标服务器不是 192.168.62.38 或目录结构与本文档不一致时

## 服务器与本地配置

### 服务器配置

| 配置项 | 值 |
|--------|-----|
| 服务器地址 | `192.168.62.38:22` |
| 登录用户 | `aiwinse02` |
| 服务器目录 | `/home/aiwinse02/公共的/Tpaip-project/` |

### 本地配置

| 配置项 | 值 |
|--------|-----|
| GitLab 仓库 | `ssh://git@192.168.6.21:49001/ai/tpaip.git` |
| 本地代码目录 | `D:\gitlap-tpaip\tpaip` |
| 分支 | `master` |

### 服务列表

| 服务名 | 镜像标签 | 端口 |
|--------|---------|------|
| tpaip-backend | `tpaip-backend:latest` | 8000 |
| tpaip-frontend | `tpaip-frontend:latest` | 3000 |
| tpaip-chromadb | `tpaip-chromadb:latest` | 8002 |
| tpaip-mcp | `tpaip-mcp:latest` | 8001 |

### 版本目录命名规则

- 版本号 `X.Y.Z` 对应目录名 `TpaipvX.Y.Z版本`
- 目录结构：`/home/aiwinse02/公共的/Tpaip-project/Tpaipv{版本号}版本/opt/tpaip/`

## The Process

### Step 1: 确认部署参数

向用户确认以下参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| 新版本号 | 部署的目标版本号 | `2.2.4` |
| 旧版本号 | 当前运行的版本号 | `2.2.3` |
| 替换 Compose | 是否上传新的 docker-compose.yml | `y/n` |

**异常处理**：如果用户提供的旧版本号对应的目录在服务器上不存在，提示用户确认版本号是否正确后再继续。

### Step 2: 拉取最新代码

在本地执行：

```bash
cd D:\gitlap-tpaip\tpaip
git pull origin master
```

**异常处理**：如果 `git pull` 失败（合并冲突、网络问题），报告错误信息并停止，提示用户手动解决后重试。

### Step 3: 构建 Docker 镜像

在本地代码目录执行（显示详细输出）：

```bash
docker compose build
```

**异常处理**：如果构建失败，报告错误日志并停止。不清理悬空镜像，由用户决定是否手动清理。

### Step 4: 打包镜像为 tar 文件

在本地执行：

```bash
docker save -o tpaip-images.tar \
  tpaip-backend:latest tpaip-frontend:latest \
  tpaip-chromadb:latest tpaip-mcp:latest
```

**注意**：确认本地磁盘空间充足（4 个镜像打包后文件通常较大）。

### Step 5: 在服务器创建新版本目录并复制旧版本

通过 SSH 在服务器上执行：

```bash
mkdir -p /home/aiwinse02/公共的/Tpaip-project/Tpaipv{新版本号}版本
cp -r /home/aiwinse02/公共的/Tpaip-project/Tpaipv{旧版本号}版本/* \
      /home/aiwinse02/公共的/Tpaip-project/Tpaipv{新版本号}版本/
```

**异常处理**：如果旧版本目录不存在，停止并提示用户检查旧版本号是否正确。

### Step 6: 停止旧版本服务

通过 SSH 在旧版本目录下执行：

```bash
cd /home/aiwinse02/公共的/Tpaip-project/Tpaipv{旧版本号}版本/opt/tpaip
docker compose down
```

**异常处理**：如果停止失败（容器未响应），尝试 `docker compose down --timeout 30`，仍失败则报告错误并停止。

### Step 7: 上传文件到服务器

通过 SCP 上传镜像文件：

```bash
scp tpaip-images.tar aiwinse02@192.168.62.38:/home/aiwinse02/公共的/Tpaip-project/Tpaipv{新版本号}版本/opt/tpaip/
```

如果 Step 1 中用户选择替换 docker-compose.yml（参数为 `y`），额外上传：

```bash
scp docker-compose.yml aiwinse02@192.168.62.38:/home/aiwinse02/公共的/Tpaip-project/Tpaipv{新版本号}版本/opt/tpaip/
```

**异常处理**：如果上传中断，提示用户手动重试 SCP，不要自动重传（避免不完整文件覆盖完整文件）。

### Step 8: 在服务器加载新镜像

通过 SSH 在新版本目录下执行：

```bash
cd /home/aiwinse02/公共的/Tpaip-project/Tpaipv{新版本号}版本/opt/tpaip
docker load -i tpaip-images.tar
```

**异常处理**：如果加载失败（tar 文件损坏或不完整），提示用户重新上传镜像文件。

### Step 9: 启动新服务

通过 SSH 执行：

```bash
cd /home/aiwinse02/公共的/Tpaip-project/Tpaipv{新版本号}版本/opt/tpaip
docker compose up -d
```

**异常处理**：如果启动失败，输出 `docker compose logs` 的内容供用户排查。

### Step 10: 健康检查

等待服务启动（建议等待 10-15 秒），通过 SSH 执行：

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

验证标准：
- 4 个容器（backend、frontend、chromadb、mcp）状态均为 `Up`
- 端口映射正确：8000、3000、8002、8001

**异常处理**：如果有容器未运行，通过 `docker logs <容器名>` 获取错误日志并报告。

### Step 11: 生成部署报告

输出以下格式的部署报告，并将完整日志保存到 `~/.claude/logs/deploy-{版本号}-{时间戳}.log`：

```
=== 部署报告 ===

项目: TPAIP
新版本: Tpaipv{新版本号}版本
旧版本: Tpaipv{旧版本号}版本
时间: {YYYY-MM-DD HH:mm:ss}

执行结果:
- 代码更新: 成功/失败
- 镜像构建: 成功/失败
- 镜像打包: 成功/失败
- 服务停止: 成功/失败
- 文件上传: 成功/失败
- 镜像加载: 成功/失败
- 服务启动: 成功/失败
- 健康检查: 成功/失败

容器状态:
- tpaip-backend (运行中/异常)
- tpaip-frontend (运行中/异常)
- tpaip-chromadb (运行中/异常)
- tpaip-mcp (运行中/异常)

部署日志: ~/.claude/logs/deploy-{版本号}-{时间戳}.log
```

## 失败处理策略

- 任何步骤失败时，立即停止并报告错误信息
- **不执行自动回滚**，由用户决定是否手动回退到旧版本
- 构建失败不自动清理悬空镜像

## 产出物规范

| 产出物 | 格式 | 说明 |
|--------|------|------|
| 部署报告 | 文本 | 包含各步骤执行结果和容器状态，输出到终端 |
| 部署日志 | 日志文件 | 保存到 `~/.claude/logs/deploy-{版本号}-{时间戳}.log` |

## 质量检查点

- [ ] `git pull` 成功，无合并冲突
- [ ] `docker compose build` 所有 4 个镜像构建成功
- [ ] `docker ps` 显示 4 个容器状态均为 `Up`
- [ ] 各服务端口映射正确（8000/3000/8002/8001）
- [ ] 部署日志已保存到 `~/.claude/logs/deploy-{版本号}-{时间戳}.log`

## Common Mistakes

| 错误做法 | 正确做法 |
|---------|---------|
| 直接覆盖旧版本目录 | 先创建新版本目录并复制旧版本内容，保留回退能力 |
| 忘记停止旧版本服务就启动新服务 | 先在旧版本目录执行 `docker compose down`，再启动新版本 |
| 忽略磁盘空间检查 | 打包前确认本地和服务器磁盘空间充足 |
| 上传中断后自动重传 | 提示用户手动重试，避免不完整文件覆盖完整文件 |
| 部署完不做健康检查 | 必须执行 Step 10 验证所有容器正常运行 |

> **注意：不要编造服务器地址、端口、用户名或目录路径。所有配置参数必须使用本文档中提供的值。如果某个配置项在本文档中未提供，停止并询问用户。**

## 变更历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|-------|---------|
| 1.0 | 2026-03-03 | 原作者 | 初版 |
| 1.1 | 2026-03-30 | TP-Skill-Refiner | 按照技象规范优化结构和质量 |
