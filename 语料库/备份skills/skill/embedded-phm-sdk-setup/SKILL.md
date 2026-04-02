---
name: embedded-phm-sdk-setup
description: PHM SDK 下载和配置
workflow_phase: setup
domain: embedded
---

# PHM SDK 配置

配置 PHM 开发所需的 SDK。

## SDK 获取

```
\\192.168.6.21\ftp\02. 安装包\02. 软件开发工具\08. PowerHarmony\sdk\PHM\PHM_SDK_V1.0.1.0\
```

文件：`PowerHarmony_PHM_SDK_V1.0.1.0.tar.gz`

## 配置步骤

### 1. 解压 SDK

```bash
cd /workspace
tar -xzf PowerHarmony_PHM_SDK_V1.0.1.0.tar.gz
```

### 2. 设置环境变量

```bash
export PHM_SDK_HOME=/workspace/PHM_SDK_V1.0.1.0
export PATH=$PHM_SDK_HOME/tools:$PATH
```

### 3. 验证 SDK

```bash
# 检查目录结构
ls $PHM_SDK_HOME

# 应该包含:
# - device/
# - kernel/
# - tools/
# - build/
```

## 验证标准

- [ ] SDK 解压成功
- [ ] 环境变量设置正确
- [ ] 目录结构完整

## 下一步

完成后使用 `phm-code-setup` 配置代码仓库。
