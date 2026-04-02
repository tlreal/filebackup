---
name: embedded-memory-optimization
description: 在资源受限的嵌入式项目中优化内存使用
workflow_phase: plan
domain: embedded
---

# Memory Optimization - 内存优化

## 概述

系统性地优化嵌入式系统的内存使用，包括 Flash 和 RAM。

## 优化策略

### 1. Flash 优化

| 策略 | 说明 |
|------|------|
| **编译器优化** | -Os 优化大小 |
| **去除未用代码** | -ffunction-sections + --gc-sections |
| **精简库** | 使用 newlib-nano |
| **常量压缩** | 压缩只读数据 |

```makefile
# 典型优化配置
CFLAGS += -Os -ffunction-sections -fdata-sections
LDFLAGS += --gc-sections
```

### 2. RAM 优化

| 策略 | 说明 |
|------|------|
| **静态分配** | 避免动态内存 |
| **栈大小调整** | 根据实际使用调整 |
| **共享缓冲区** | 多功能复用同一缓冲 |
| **位域压缩** | 使用 bit field |

```c
// 位域示例
typedef struct {
    uint8_t flag1 : 1;
    uint8_t flag2 : 1;
    uint8_t state : 3;
    uint8_t reserved : 3;
} compact_flags_t;  // 仅 1 字节
```

### 3. 内存池

```c
// 固定大小内存池
#define POOL_BLOCK_SIZE  64
#define POOL_BLOCK_COUNT 16

static uint8_t pool_memory[POOL_BLOCK_SIZE * POOL_BLOCK_COUNT];
static uint8_t pool_used[POOL_BLOCK_COUNT];

void* pool_alloc(void) {
    for (int i = 0; i < POOL_BLOCK_COUNT; i++) {
        if (!pool_used[i]) {
            pool_used[i] = 1;
            return &pool_memory[i * POOL_BLOCK_SIZE];
        }
    }
    return NULL;
}
```

## 分析工具

### 编译后分析
```bash
# 查看段大小
arm-none-eabi-size app.elf

# 查看符号大小
arm-none-eabi-nm --size-sort app.elf | tail -20
```

### 运行时分析
```c
// 栈水位检测
void check_stack_usage(void) {
    extern uint32_t _estack, _Min_Stack_Size;
    uint32_t *stack_start = (uint32_t*)(&_estack - &_Min_Stack_Size);
    uint32_t used = 0;
    for (uint32_t *p = stack_start; *p != 0xDEADBEEF; p++) {
        used++;
    }
    printf("Stack used: %lu bytes\n", used * 4);
}
```

## 输出格式

```yaml
内存优化报告:
  优化前:
    Flash: 128KB / 256KB (50%)
    RAM: 48KB / 64KB (75%)
    
  优化后:
    Flash: 96KB / 256KB (37%)  # 节省 32KB
    RAM: 32KB / 64KB (50%)     # 节省 16KB
    
  优化措施:
    - 启用 -Os 编译优化
    - 移除未使用函数
    - 使用 newlib-nano
    - 静态分配替代 malloc
```

## 与 Core Workflow 集成

**在 Plan 阶段考虑:**
- 在 `writing-plans` 时规划内存预算
- 作为任务的验收标准之一

**在 Act 阶段应用:**
- 实现时遵循优化策略
- 验证时检查内存使用
