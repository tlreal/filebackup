---
name: embedded-phm-overview
description: 电鸿PHM（TP1502）开发环境搭建概览，介绍整体流程、所需资源
workflow_phase: setup
domain: embedded
dependencies:
  - phm-docker-setup
  - phm-sdk-setup
  - phm-code-setup
  - phm-compile
---

# 电鸿 PHM（TP1502）环境搭建概览

电鸿 PHM 开发环境搭建指南入口。

## 🎯 目标环境

| 项目 | 说明 |
|------|------|
| **芯片** | TP1502 |
| **厂商** | ASR + Techphant |
| **操作系统** | Ubuntu 24.02 |
| **SDK 版本** | PHM_SDK_V1.0.1.0 |
| **开发模式** | Docker 容器化开发 |

## ⏱️ 时间估算

- **完整流程**：约 3-4 小时
- **分步完成**：
  - 环境检查 + Docker 配置：1-2小时
  - SDK 和代码配置：1-2小时
  - 编译验证：30分钟

## 📦 所需资源

### Docker 镜像（约 2-3GB）
```
\\192.168.6.21\ftp\02. 安装包\02. 软件开发工具\08. PowerHarmony\sdk\PHM\PHM_SDK_V1.0.1.0\docker\24.1111\
```
推荐版本：24.1111（内置hb工具，无需外网）

### SDK（约 500MB）
```
\\192.168.6.21\ftp\02. 安装包\02. 软件开发工具\08. PowerHarmony\sdk\PHM\PHM_SDK_V1.0.1.0\
```

### 代码仓库
需要访问公司 Git 服务器（192.168.6.21:49001）

## 🎓 搭建流程

1. **环境检查** → `phm-check-env`
2. **Docker 配置** → `phm-docker-setup`
3. **SDK 配置** → `phm-sdk-setup`
4. **代码配置** → `phm-code-setup`
5. **编译验证** → `phm-compile`

## 📊 完成标准

- ✅ Docker 容器可以正常启动
- ✅ hb set 可以选择 tp1502
- ✅ hb build 编译成功
- ✅ 可以导出固件文件

## ⚠️ 注意事项

- **系统要求**：Ubuntu 24.02，全新安装推荐
- **内存**：至少 8GB（推荐 16GB）
- **磁盘**：至少 50GB 可用空间
- **网络**：内网访问 192.168.6.21

## 与 Core Workflow 集成

**作为前置条件:**
- 在开始 PHM 项目前完成所有子步骤
- 验证后进入 Think 阶段
