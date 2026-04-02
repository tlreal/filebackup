---
name: foundation-platform-config
description: 提供平台配置信息，被其他Skills调用以获取平台特定参数
---

# Platform Config - 平台配置

## 概述

提供嵌入式平台的配置信息，作为其他 Skills 的数据来源。

## 支持的平台

### STM32 系列

```yaml
stm32f1:
  name: STM32F1 Series
  core: Cortex-M3
  max_freq: 72MHz
  hal: STM32Cube HAL
  ide: 
    - Keil MDK
    - STM32CubeIDE
  debug: SWD, JTAG

stm32f4:
  name: STM32F4 Series
  core: Cortex-M4F
  max_freq: 168MHz
  hal: STM32Cube HAL
  features:
    - FPU
    - DSP
  
stm32h7:
  name: STM32H7 Series
  core: Cortex-M7
  max_freq: 480MHz
  features:
    - Dual Core (部分型号)
    - 高速缓存
```

### ESP32 系列

```yaml
esp32:
  name: ESP32
  core: Xtensa LX6 (Dual)
  max_freq: 240MHz
  framework: ESP-IDF
  features:
    - WiFi
    - Bluetooth

esp32-s3:
  name: ESP32-S3
  core: Xtensa LX7 (Dual)
  max_freq: 240MHz
  framework: ESP-IDF
  features:
    - WiFi 6
    - BLE 5.0
    - AI 加速
```

### NXP 系列

```yaml
lpc1768:
  name: LPC1768
  core: Cortex-M3
  max_freq: 100MHz
  hal: LPCOpen
  
rt1050:
  name: i.MX RT1050
  core: Cortex-M7
  max_freq: 600MHz
```

## 使用方式

其他 Skills 可以引用此配置：

```markdown
当选择平台时，参考 `foundation-platform-config` 获取：
- 支持的开发环境
- HAL/SDK 版本
- 调试接口
```

## 扩展

添加新平台时，在此文件中添加配置信息：

```yaml
new_platform:
  name: Platform Name
  core: Core Type
  max_freq: XXXMHz
  hal: HAL Name
  ide:
    - IDE1
    - IDE2
  features:
    - Feature1
    - Feature2
```
