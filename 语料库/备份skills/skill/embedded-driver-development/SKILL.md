---
name: embedded-driver-development
description: 在开发硬件驱动程序时使用，包括外设驱动和传感器驱动
workflow_phase: act
domain: embedded
---

# Driver Development - 驱动开发

## 概述

系统性地开发硬件驱动程序，确保可移植性、可测试性和可维护性。

## 驱动分层架构

```
┌─────────────────────────────────────┐
│  Application Layer (应用层)          │
│  - 业务逻辑                          │
├─────────────────────────────────────┤
│  Driver Layer (驱动层)               │
│  - 设备抽象接口                       │
│  - 状态机和流程控制                   │
├─────────────────────────────────────┤
│  HAL Layer (硬件抽象层)              │
│  - 寄存器操作封装                     │
│  - 平台相关代码                       │
├─────────────────────────────────────┤
│  Hardware (硬件)                     │
└─────────────────────────────────────┘
```

## 开发流程

### 1. 理解硬件

- 阅读数据手册的相关章节
- 理解寄存器配置
- 确认电气特性和时序要求

### 2. 设计接口

```c
// driver_xxx.h - 驱动层接口示例

typedef enum {
    DRV_XXX_OK = 0,
    DRV_XXX_ERROR,
    DRV_XXX_BUSY,
    DRV_XXX_TIMEOUT
} drv_xxx_status_t;

// 初始化
drv_xxx_status_t drv_xxx_init(const drv_xxx_config_t *config);

// 操作接口
drv_xxx_status_t drv_xxx_read(uint8_t *data, uint32_t len);
drv_xxx_status_t drv_xxx_write(const uint8_t *data, uint32_t len);

// 状态查询
bool drv_xxx_is_ready(void);
```

### 3. 实现 HAL 层

```c
// driver_xxx_port.h - HAL 层接口

// 平台相关初始化
void xxx_port_init(void);

// 底层读写
void xxx_port_spi_transfer(uint8_t *tx, uint8_t *rx, uint32_t len);
void xxx_port_delay_ms(uint32_t ms);
void xxx_port_gpio_set(bool level);
```

### 4. 实现驱动层

遵循 TDD：
1. 写失败的测试
2. 实现最小代码
3. 验证通过
4. 重构

### 5. 集成测试

- 在目标硬件上运行
- 验证功能正确
- 验证时序符合要求

## 最佳实践

### 可移植性

- HAL 层隔离所有平台相关代码
- 使用回调函数处理异步事件
- 避免硬编码魔法数字

### 错误处理

- 返回值明确指示状态
- 提供详细的错误信息
- 支持错误恢复

### 资源管理

- 显式初始化和反初始化
- 避免动态内存分配
- 注意中断上下文限制

## 输出清单

- [ ] `driver_xxx.h` - 驱动层头文件
- [ ] `driver_xxx.c` - 驱动层实现
- [ ] `driver_xxx_port.h` - HAL 层头文件
- [ ] `driver_xxx_port_{platform}.c` - 平台实现
- [ ] `test_driver_xxx.c` - 单元测试
- [ ] `README.md` - 使用说明

## 与 Core Workflow 集成

**在 Act 阶段调用:**
- 当执行计划中包含驱动开发任务时
- 配合 `core-test-driven-development` 使用

**前置 Skills:**
- `embedded-datasheet-analysis` - 理解硬件
- `embedded-module-design` - 设计接口
