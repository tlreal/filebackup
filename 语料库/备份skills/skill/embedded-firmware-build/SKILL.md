---
name: embedded-firmware-build
description: 构建嵌入式固件，生成可烧录的二进制文件
workflow_phase: act
domain: embedded
---

# Firmware Build - 固件构建

## 概述

构建嵌入式项目，生成可烧录到目标硬件的固件文件。

## 构建系统

### Make
```makefile
# 典型 Makefile 结构
TARGET = firmware
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy

CFLAGS = -mcpu=cortex-m4 -mthumb -Os
LDFLAGS = -T linker.ld -Wl,--gc-sections

SRCS = $(wildcard src/*.c)
OBJS = $(SRCS:.c=.o)

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

$(TARGET).elf: $(OBJS)
	$(CC) $(LDFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET).elf $(TARGET).bin
```

### CMake
```cmake
cmake_minimum_required(VERSION 3.16)
project(firmware C)

set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_C_FLAGS "-mcpu=cortex-m4 -mthumb -Os")

add_executable(${PROJECT_NAME}.elf
    src/main.c
    src/startup.c
)

# 生成 bin 文件
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary 
            ${PROJECT_NAME}.elf ${PROJECT_NAME}.bin
)
```

## 构建流程

```
源代码
   ↓
预处理 (.c → .i)
   ↓
编译 (.i → .s)
   ↓
汇编 (.s → .o)
   ↓
链接 (.o → .elf)
   ↓
生成二进制 (.elf → .bin/.hex)
   ↓
固件验证
```

## 构建验证

### 大小检查
```bash
arm-none-eabi-size firmware.elf
# 输出:
#    text    data     bss     dec     hex filename
#   12345     456    1024   13825    3601 firmware.elf
```

### 符号检查
```bash
arm-none-eabi-nm -S --size-sort firmware.elf | tail -10
```

### Map 文件分析
```bash
arm-none-eabi-gcc ... -Wl,-Map=firmware.map
# 分析 map 文件了解内存布局
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| undefined reference | 缺少实现/库 | 检查链接顺序 |
| Flash 溢出 | 代码太大 | 优化/裁剪 |
| RAM 溢出 | 数据太多 | 使用 const/优化 |
| 启动失败 | 链接脚本错误 | 检查内存映射 |

## 输出清单

- [ ] `firmware.elf` - 调试用
- [ ] `firmware.bin` - 烧录用
- [ ] `firmware.hex` - 烧录用（可选）
- [ ] `firmware.map` - 分析用
- [ ] 构建日志

## 与 Core Workflow 集成

**在 Act 阶段调用:**
- 代码实现完成后
- 准备进行硬件测试前

**后续步骤:**
- 使用 `hardware-debug` 烧录和调试
- 使用 `release-checklist` 准备发布
