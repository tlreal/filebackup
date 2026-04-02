---
name: embedded-phm-compile
description: PHM 项目编译流程
workflow_phase: setup
domain: embedded
---

# PHM 编译

PHM 项目的编译构建流程。

## 编译步骤

### 1. 进入 Docker 容器

```bash
docker exec -it phm_dev bash
cd /workspace/PHM_SDK_V1.0.1.0
```

### 2. 选择目标配置

```bash
hb set
# 选择 tp1502
```

### 3. 执行编译

```bash
hb build
```

### 4. 查看输出

```bash
# 编译输出位置
ls out/tp1502/

# 固件文件
ls out/tp1502/images/
```

## 编译选项

| 命令 | 说明 |
|------|------|
| `hb build` | 完整编译 |
| `hb build -f` | 强制重新编译 |
| `hb clean` | 清理编译产物 |

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| hb 命令未找到 | 检查 Docker 镜像版本 |
| 编译错误 | 查看具体错误信息 |
| 内存不足 | 关闭其他程序或增加内存 |

## 验证标准

- [ ] `hb set` 可以选择 tp1502
- [ ] `hb build` 编译成功无错误
- [ ] 固件文件生成在 out/ 目录

## 完成

编译成功后，PHM 环境搭建完成！可以开始项目开发。
