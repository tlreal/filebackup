---
name: simulation-coding
description: 在进行通信仿真系统代码实现时使用 - 提供编码规范、AI辅助编码方法和代码优化策略
---

# Simulation Coding - 仿真系统代码实现

## 概述

通信仿真系统代码实现需要关注算法正确性、性能优化和代码可维护性。

**核心原则:** 正确性优先 + 性能优化 + 规范编码

## 何时使用

- 根据详细设计进行代码实现
- 实现调制解调算法
- 编写单元测试
- 进行代码优化

## 编码规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 函数名 | 动词开头，驼峰命名 | `modulateFSK`, `demodulateSignal` |
| 变量名 | 名词，有意义 | `carrierFreq`, `symbolRate` |
| 常量名 | 全大写，下划线分隔 | `MAX_SAMPLE_RATE`, `DEFAULT_FREQ` |
| 类名 | 首字母大写 | `FSKModulator`, `SignalProcessor` |

### 代码结构规范

```matlab
function [output] = functionName(input1, input2)
%FUNCTIONNAME 简要功能描述
%   详细功能描述
%
%   输入参数:
%       input1 - 参数1说明
%       input2 - 参数2说明
%
%   输出参数:
%       output - 输出说明
%
%   示例:
%       result = functionName(data, config);

    % 参数验证
    validateInputs(input1, input2);
    
    % 核心处理逻辑
    output = processData(input1, input2);
    
end
```

## AI 辅助编码

### 代码生成提示词

```
请帮我实现 [功能名称]，要求：
1. 技术规格：
   - 调制方式：2FSK
   - 载波频率：1kHz/2kHz
   - 符号速率：100bps
   - 采样率：10kHz
   
2. 接口要求：
   - 输入：比特流 (0/1数组)
   - 输出：调制信号 (复信号)
   
3. 性能要求：
   - 处理时延 < 10ms
   - 内存占用 < 100MB
   
4. 代码规范：
   - 添加完整注释
   - 包含参数验证
   - 处理边界情况
```

### 代码优化提示词

```
请优化以下代码的性能：
[代码片段]

优化目标：
1. 减少计算时间
2. 降低内存占用
3. 保持代码可读性

请提供：
1. 优化后的代码
2. 优化点说明
3. 性能提升预估
```

## 性能优化策略

### 向量化优化

```matlab
% 优化前：循环实现
for i = 1:length(data)
    result(i) = sin(2*pi*freq*t(i));
end

% 优化后：向量化实现
result = sin(2*pi*freq*t);
```

### 并行计算优化

```matlab
% 使用 parfor 并行处理
parfor i = 1:numSimulations
    results{i} = runSimulation(params(i));
end
```

### 内存优化

```matlab
% 预分配内存
output = zeros(1, signalLength);

% 分块处理大数据
for chunk = 1:numChunks
    data = loadChunk(chunk);
    processChunk(data);
end
```

## 单元测试规范

### 测试用例设计

```matlab
function tests = testFSKModulation
    tests = functiontests(localfunctions);
end

function testBasicModulation(testCase)
    % 测试基本调制功能
    bits = [0 1 0 1];
    params = getDefaultParams();
    
    signal = modulateFSK(bits, params);
    
    % 验证输出长度
    expectedLength = length(bits) * params.samplesPerSymbol;
    verifyEqual(testCase, length(signal), expectedLength);
end

function testBoundaryConditions(testCase)
    % 测试边界条件
    emptyBits = [];
    params = getDefaultParams();
    
    signal = modulateFSK(emptyBits, params);
    
    verifyEmpty(testCase, signal);
end
```

### 测试覆盖要求

- [ ] 正常情况测试
- [ ] 边界条件测试
- [ ] 异常输入测试
- [ ] 性能基准测试

## 代码审查检查清单

### 正确性检查
- [ ] 算法逻辑是否正确
- [ ] 边界条件是否处理
- [ ] 异常情况是否处理
- [ ] 数值精度是否满足

### 性能检查
- [ ] 是否使用向量化
- [ ] 是否避免不必要的循环
- [ ] 内存使用是否合理
- [ ] 是否有性能瓶颈

### 规范性检查
- [ ] 命名是否规范
- [ ] 注释是否完整
- [ ] 代码结构是否清晰
- [ ] 是否遵循编码规范

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 性能不达标 | 向量化、并行化、算法优化 |
| 数值精度问题 | 使用双精度、检查舍入误差 |
| 内存溢出 | 分块处理、及时释放内存 |
| 调试困难 | 添加日志、分模块调试 |
