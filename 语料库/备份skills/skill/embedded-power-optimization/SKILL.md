---
name: embedded-power-optimization
description: 优化嵌入式系统功耗，延长电池寿命
workflow_phase: plan
domain: embedded
---

# Power Optimization - 功耗优化

## 概述

系统性地优化嵌入式系统功耗，特别适用于电池供电设备。

## 功耗模型

```
总功耗 = 静态功耗 + 动态功耗

动态功耗 ∝ C × V² × f
- C: 负载电容
- V: 供电电压
- f: 工作频率
```

## 优化策略

### 1. 电源模式管理

| 模式 | 典型电流 | 唤醒时间 | 适用场景 |
|------|---------|---------|---------|
| Run | ~100mA | - | 正常工作 |
| Sleep | ~1mA | <1ms | 短暂等待 |
| Stop | ~10uA | ~ms | 长时间等待 |
| Standby | ~1uA | ~10ms | 极低功耗 |

### 2. 时钟管理

```c
// 动态调频示例
void enter_low_power_mode(void) {
    // 降低系统时钟
    SystemClock_Config_LowPower();
    
    // 关闭未使用外设时钟
    __HAL_RCC_GPIOB_CLK_DISABLE();
    __HAL_RCC_USART2_CLK_DISABLE();
}

void exit_low_power_mode(void) {
    // 恢复系统时钟
    SystemClock_Config_Normal();
    
    // 恢复外设时钟
    __HAL_RCC_GPIOB_CLK_ENABLE();
}
```

### 3. 外设管理

- 不用的外设关闭
- GPIO 配置为低功耗状态
- 使用 DMA 减少 CPU 唤醒

### 4. 软件优化

- 减少轮询，使用中断
- 批量处理数据
- 优化算法减少计算

## 功耗测量

### 测量方法
```
电源 → 采样电阻(如10Ω) → 设备
         ↓
      示波器/万用表
      测量电压降
```

### 计算公式
```
I = V_resistor / R_sample
P = V_supply × I
```

## 输出格式

```yaml
功耗优化报告:
  目标:
    待机电流: < 10uA
    工作电流: < 50mA
    电池寿命: > 1年 (2000mAh)
    
  测量结果:
    待机电流: 8uA ✅
    工作电流: 45mA ✅
    
  优化措施:
    - 使用 Stop 模式替代 Sleep
    - 关闭未使用 GPIO
    - 降低 ADC 采样率
    
  电池寿命估算:
    待机占比: 99%
    平均电流: 8uA × 99% + 45mA × 1% = 458uA
    电池寿命: 2000mAh / 458uA ≈ 4370小时 ≈ 182天
```

## 与 Core Workflow 集成

**在 Plan 阶段考虑:**
- 在 `writing-plans` 时规划功耗预算
- 确定低功耗模式使用策略

**在 Act 阶段应用:**
- 实现电源管理模块
- 验证功耗指标
