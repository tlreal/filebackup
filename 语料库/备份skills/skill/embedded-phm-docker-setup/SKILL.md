---
name: embedded-phm-docker-setup
description: PHM 开发环境的 Docker 容器配置
workflow_phase: setup
domain: embedded
---

# PHM Docker 配置

配置 PHM 开发所需的 Docker 容器环境。

## 前置条件

- Ubuntu 24.02 系统
- Docker 已安装
- 可访问 192.168.6.21 FTP

## 配置步骤

### 1. 获取 Docker 镜像

```bash
# 从 FTP 下载镜像文件
# 位置: \\192.168.6.21\ftp\...\docker\24.1111\powerharmony_phm_sdk_v1.0.1.0_24.1111.tar.gz

# 加载镜像
docker load -i powerharmony_phm_sdk_v1.0.1.0_24.1111.tar.gz
```

### 2. 创建容器

```bash
docker run -it \
    --name phm_dev \
    -v /home/$USER/phm:/workspace \
    powerharmony_phm_sdk:v1.0.1.0_24.1111 \
    /bin/bash
```

### 3. 验证容器

```bash
# 进入容器
docker exec -it phm_dev bash

# 检查 hb 工具
hb --version
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `docker start phm_dev` | 启动容器 |
| `docker stop phm_dev` | 停止容器 |
| `docker exec -it phm_dev bash` | 进入容器 |

## 验证标准

- [ ] `docker images` 显示镜像
- [ ] 容器可以正常启动
- [ ] 容器内 `hb --version` 正常

## 下一步

完成后使用 `phm-sdk-setup` 配置 SDK。
