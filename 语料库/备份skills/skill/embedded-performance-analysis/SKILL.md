---
name: embedded-performance-analysis
description: 分析嵌入式系统性能，包括CPU占用、响应时间等
workflow_phase: act
domain: embedded
---

# Performance Analysis - 性能分析

## 概述

分析嵌入式系统的运行时性能，识别瓶颈并优化。

## 性能指标

| 指标 | 说明 | 目标值示例 |
|------|------|-----------|
| **CPU 占用** | 平均/峰值 | < 70% |
| **响应时间** | 最大延迟 | < 10ms |
| **内存使用** | 峰值/平均 | < 80% |
| **中断延迟** | 最大时间 | < 100us |

## 测量方法

### 1. CPU 占用

```c
// 空闲任务计数法
volatile uint32_t idle_counter = 0;

void idle_task(void) {
    while(1) {
        idle_counter++;
    }
}

// 计算 CPU 使用率
float cpu_usage = 1.0 - (float)idle_counter / max_counter;
```

### 2. 时间测量

```c
// GPIO 翻转 + 示波器
#define PROFILE_START() HAL_GPIO_WritePin(GPIOA, GPIO_PIN_0, 1)
#define PROFILE_END()   HAL_GPIO_WritePin(GPIOA, GPIO_PIN_0, 0)

void critical_function(void) {
    PROFILE_START();
    // 被测代码
    PROFILE_END();
}
```

### 3. 定时器测量

```c
uint32_t start = get_systick();
// 被测代码
uint32_t end = get_systick();
uint32_t duration_us = (end - start) * tick_period_us;
```

## 分析工具

| 工具 | 用途 |
|------|------|
| 示波器 | 精确时序 |
| 逻辑分析仪 | 多信号分析 |
| 串口日志 | 事件追踪 |
| IDE Profiler | 代码分析 |

## 优化策略

### 代码优化
- 减少函数调用开销
- 使用查表替代计算
- 循环展开

### 算法优化
- 选择更高效算法
- 减少不必要计算
- 利用硬件加速

### 系统优化
- 调整任务优先级
- 优化中断处理
- 使用 DMA

## 输出格式

```yaml
性能分析报告:
  测试环境:
    芯片: STM32F407
    主频: 168MHz
    编译优化: O2
    
  测试结果:
    CPU占用:
      平均: 45%
      峰值: 72%
    响应时间:
      平均: 2.5ms
      最大: 8.3ms
    内存使用:
      Flash: 78%
      RAM: 62%
      
  瓶颈分析:
    - 函数A 占用 25% CPU
    - 中断B 延迟过高
    
  优化建议:
    - 优化函数A 算法
    - 减少中断B处理时间
```

## 与 Core Workflow 集成

**在 Act 阶段调用:**
- 功能完成后进行性能验证
- 作为 `verification` 的一部分
