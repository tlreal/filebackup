---
name: embedded-env-setup
description: 搭建嵌入式开发环境，包括工具链、IDE和调试工具
workflow_phase: setup
domain: embedded
---

# Env Setup - 环境搭建

## 概述

搭建完整的嵌入式开发环境，确保可以编译、调试和烧录。

## 环境组成

```
开发环境
├── 编译器/工具链
│   ├── ARM: arm-none-eabi-gcc
│   ├── ESP: xtensa-esp32-elf
│   └── RISC-V: riscv-none-embed-gcc
├── IDE
│   ├── Keil MDK
│   ├── STM32CubeIDE
│   ├── VS Code + 插件
│   └── ESP-IDF 插件
├── 调试工具
│   ├── OpenOCD
│   ├── J-Link
│   └── ST-Link
└── 辅助工具
    ├── Git
    ├── Make/CMake
    └── Python
```

## 平台特定指南

### STM32 环境

**方式一: Keil MDK**
- 安装 Keil MDK5
- 安装对应 PACK
- 配置调试器

**方式二: STM32CubeIDE**
- 下载并安装 STM32CubeIDE
- 自带 GCC 工具链和 STLink 驱动

**方式三: VS Code + 命令行**
```bash
# 安装工具链
sudo apt install gcc-arm-none-eabi
# 或 Windows 从 ARM 官网下载

# 安装 OpenOCD
sudo apt install openocd
```

### ESP32 环境

```bash
# 1. 安装 ESP-IDF
mkdir -p ~/esp
cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git

# 2. 安装工具链
cd esp-idf
./install.sh

# 3. 设置环境变量
. ./export.sh
```

## 环境验证

### 检查清单

- [ ] 编译器可用: `arm-none-eabi-gcc --version`
- [ ] 构建工具可用: `make --version`
- [ ] 调试器可用: `openocd --version`
- [ ] 可以编译示例项目
- [ ] 可以下载到目标板
- [ ] 可以调试（断点、单步）

### 验证脚本

```bash
#!/bin/bash
echo "检查开发环境..."

# 检查编译器
if command -v arm-none-eabi-gcc &> /dev/null; then
    echo "✅ ARM GCC: $(arm-none-eabi-gcc --version | head -1)"
else
    echo "❌ ARM GCC 未安装"
fi

# 检查 Make
if command -v make &> /dev/null; then
    echo "✅ Make: $(make --version | head -1)"
else
    echo "❌ Make 未安装"
fi

# ... 更多检查
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 找不到编译器 | PATH 未设置 | 添加到 PATH |
| 无法识别设备 | 驱动问题 | 安装驱动 |
| 下载失败 | 连接问题 | 检查硬件连接 |
| 调试失败 | 配置错误 | 检查调试器配置 |

## 与 Core Workflow 集成

**作为前置条件:**
- 在开始任何 Think/Plan/Act 之前
- 确保环境可用

**输出:**
- 环境验证报告
- 可以继续进入 Think 阶段
