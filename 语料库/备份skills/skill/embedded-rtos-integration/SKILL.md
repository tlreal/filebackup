---
name: embedded-rtos-integration
description: 集成实时操作系统到嵌入式项目
workflow_phase: act
domain: embedded
---

# RTOS Integration - RTOS 集成

## 概述

将实时操作系统集成到嵌入式项目中，包括任务设计、同步机制和资源管理。

## 常见 RTOS

| RTOS | 特点 | 适用场景 |
|------|------|---------|
| **FreeRTOS** | 开源、广泛使用 | 通用嵌入式 |
| **RT-Thread** | 国产、生态好 | 物联网设备 |
| **uC/OS-III** | 商业、认证多 | 安全关键 |
| **ThreadX** | 微软、认证全 | 商业产品 |

## 任务设计

### 任务优先级原则

```
最高优先级: 硬实时任务（中断相关）
    ↓
高优先级: 通信任务（快速响应）
    ↓
中优先级: 业务任务（主逻辑）
    ↓
低优先级: 非关键任务（日志、监控）
    ↓
最低优先级: 空闲任务
```

### 任务创建

```c
// FreeRTOS 示例
void vMainTask(void *pvParameters) {
    for (;;) {
        // 任务逻辑
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void app_main(void) {
    xTaskCreate(
        vMainTask,       // 任务函数
        "main",          // 任务名称
        2048,            // 栈大小
        NULL,            // 参数
        5,               // 优先级
        NULL             // 任务句柄
    );
}
```

## 同步机制

### 信号量
```c
SemaphoreHandle_t xSemaphore = xSemaphoreCreateBinary();

// 生产者
xSemaphoreGive(xSemaphore);

// 消费者
if (xSemaphoreTake(xSemaphore, portMAX_DELAY) == pdTRUE) {
    // 获取成功
}
```

### 消息队列
```c
QueueHandle_t xQueue = xQueueCreate(10, sizeof(msg_t));

// 发送
xQueueSend(xQueue, &msg, portMAX_DELAY);

// 接收
xQueueReceive(xQueue, &msg, portMAX_DELAY);
```

### 互斥锁
```c
SemaphoreHandle_t xMutex = xSemaphoreCreateMutex();

xSemaphoreTake(xMutex, portMAX_DELAY);
// 临界区
xSemaphoreGive(xMutex);
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 栈溢出 | 栈太小 | 增大栈 / 检查深度 |
| 优先级反转 | 锁竞争 | 使用优先级继承 |
| 死锁 | 锁顺序错误 | 统一获取顺序 |
| 饥饿 | 优先级不当 | 调整优先级 |

## 最佳实践

1. **任务保持简单** - 单一职责
2. **避免长时间阻塞** - 超时机制
3. **最小化临界区** - 减少锁持有时间
4. **使用消息传递** - 优于共享内存
5. **监控栈使用** - 定期检查水位

## 与 Core Workflow 集成

**在 Act 阶段调用:**
- 在 `architecture-design` 确定使用 RTOS 后
- 作为系统集成的关键步骤

**配合使用:**
- `hardware-debug` - 调试多任务问题
- `performance-analysis` - 分析任务调度
