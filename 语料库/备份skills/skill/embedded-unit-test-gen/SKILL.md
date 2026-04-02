---
name: embedded-unit-test-gen
description: 为嵌入式代码生成单元测试
workflow_phase: act
domain: embedded
---

# Unit Test Gen - 单元测试生成

## 概述

为嵌入式代码生成高质量的单元测试，支持在主机上运行。

## 测试框架选择

| 框架 | 语言 | 特点 |
|------|------|------|
| **Unity** | C | 轻量，嵌入式首选 |
| **CppUTest** | C/C++ | 功能丰富 |
| **Google Test** | C++ | 功能强大 |
| **Ceedling** | C | Unity + 构建系统 |

## 测试结构

### 目录组织
```
project/
├── src/
│   ├── module_a.c
│   └── module_a.h
├── tests/
│   ├── test_module_a.c
│   ├── mocks/
│   │   └── mock_hal.c
│   └── unity/
│       ├── unity.c
│       └── unity.h
└── Makefile.test
```

### 测试文件模板

```c
#include "unity.h"
#include "module_a.h"

void setUp(void) {
    // 每个测试前运行
}

void tearDown(void) {
    // 每个测试后运行
}

void test_function_normal_case(void) {
    // Arrange
    int input = 5;
    int expected = 10;
    
    // Act
    int result = function_under_test(input);
    
    // Assert
    TEST_ASSERT_EQUAL(expected, result);
}

void test_function_edge_case(void) {
    // 边界条件测试
    TEST_ASSERT_EQUAL(0, function_under_test(0));
}

void test_function_error_case(void) {
    // 错误处理测试
    TEST_ASSERT_EQUAL(-1, function_under_test(-1));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_function_normal_case);
    RUN_TEST(test_function_edge_case);
    RUN_TEST(test_function_error_case);
    return UNITY_END();
}
```

## Mock 策略

### 硬件隔离

```c
// mock_hal.h
#ifndef MOCK_HAL_H
#define MOCK_HAL_H

// Mock HAL 函数
void mock_gpio_write(int pin, int value);
int mock_gpio_read(int pin);

// 设置期望值
void mock_gpio_expect_read(int pin, int return_value);

// 验证调用
void mock_gpio_verify(void);

#endif
```

### 依赖注入

```c
// 可测试的设计
typedef struct {
    void (*gpio_write)(int pin, int value);
    int (*gpio_read)(int pin);
} hal_interface_t;

void module_init(const hal_interface_t *hal);
```

## 测试覆盖目标

| 类型 | 覆盖率目标 |
|------|-----------|
| 业务逻辑 | > 80% |
| 驱动层 | > 60% |
| HAL 层 | 通过集成测试 |

## 与 Core Workflow 集成

**遵循 TDD:**
- 按照 `core-test-driven-development` 先写测试
- 测试必须先失败再通过

**验证阶段:**
- 作为 `core-verification` 的一部分
- 测试通过是完成的前提条件
