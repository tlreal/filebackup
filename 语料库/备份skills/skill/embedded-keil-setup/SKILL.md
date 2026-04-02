---
name: embedded-keil-setup
description: Keil MDK5 安装和配置完整流程，包括IDE安装、PACK文件安装和验证
workflow_phase: setup
domain: embedded
---

# Keil MDK 环境搭建指南

本 Skill 将指导你在 Windows 系统上完成 Keil MDK5 开发环境的搭建。

## 📋 环境要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 7/8/10/11 |
| **权限** | 管理员权限 |
| **网络** | 公司内网 (192.168.6.21) |
| **磁盘空间** | 至少 5GB |

## 🎯 搭建步骤

### 1. 下载安装包

```
\\192.168.6.21\ftp\02. 安装包\02. 软件开发工具\02. 单片机开发\04. Keil IDE\MDK529.exe
```

### 2. 安装 Keil MDK5

1. 关闭杀毒软件
2. 以管理员身份运行 `MDK529.exe`
3. 接受许可协议
4. 使用默认安装路径 `C:\Keil_v5`
5. 全选安装组件
6. 等待安装完成（5-10分钟）

### 3. 安装 PACK 文件

PACK 文件包含特定芯片的设备支持包。

1. 打开 Keil μVision
2. 菜单栏 → Help → Pack Installer
3. 在左侧找到目标芯片
4. 右键 → Install

**常见 PACK：**
- STM32 系列：`Keil::STM32xxx_DFP`
- NXP LPC 系列：`Keil::LPCxxx_DFP`

### 4. 验证安装

- [ ] Help → About μVision 显示 MDK 5.29
- [ ] Pack Installer 中目标 PACK 显示绿色
- [ ] 可以创建新项目并选择芯片

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| 安装失败 | 完全卸载后以管理员重装 |
| 找不到 PACK | 从 Keil 官网下载 |
| 编译错误 | 确认 PACK 版本匹配 |

## 与 Core Workflow 集成

**作为前置条件:**
- 在开始 STM32/ARM 项目前完成
- 验证后进入 Think 阶段
