---
name: embedded-tuya-t5-setup
description: TuyaOS T5 芯片开发环境搭建
workflow_phase: setup
domain: embedded
---

# TuyaOS T5 环境搭建

TuyaOS T5 芯片开发环境配置指南。

## 环境要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Ubuntu 20.04/22.04 |
| **Python** | 3.8+ |
| **芯片** | T5 系列 |

## 搭建步骤

### 1. 获取 SDK

从涂鸦开发者平台获取 TuyaOS SDK。

```bash
# 克隆 SDK
git clone https://github.com/tuya/tuya-iotos-embeded-sdk
cd tuya-iotos-embeded-sdk
```

### 2. 安装依赖

```bash
# 安装编译工具链
sudo apt install gcc-arm-none-eabi
sudo apt install cmake ninja-build

# 安装 Python 依赖
pip install -r requirements.txt
```

### 3. 配置环境

```bash
# 设置环境变量
source export.sh

# 或添加到 .bashrc
echo 'source /path/to/sdk/export.sh' >> ~/.bashrc
```

### 4. 编译验证

```bash
# 选择芯片型号
make menuconfig

# 编译
make all
```

## 验证标准

- [ ] SDK 克隆成功
- [ ] 工具链安装正确
- [ ] 可以编译示例项目

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| 工具链未找到 | 检查 PATH 设置 |
| 编译失败 | 检查依赖是否完整 |
| 权限问题 | 使用 sudo 或修改权限 |

## 与 Core Workflow 集成

**作为前置条件:**
- 在开始 TuyaOS 项目前完成
- 验证后进入 Think 阶段
