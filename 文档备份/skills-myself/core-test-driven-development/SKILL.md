---
name: core-test-driven-development
description: 在实现任何功能或修复bug时使用，在编写实现代码之前
---

# Test-Driven Development (TDD) - 测试驱动开发

## 概述

先写测试。看它失败。写最少的代码让它通过。

**核心原则:** 如果你没有看到测试失败，你不知道它是否测试了正确的东西。

**违反规则的字面意思就是违反规则的精神。**

## 何时使用

**始终使用于:**
- 新功能
- Bug 修复
- 重构
- 行为变更

**例外（需询问用户）:**
- 一次性原型
- 生成的代码
- 配置文件

在想「就这一次跳过 TDD」？停下。那是自我欺骗。

## 铁律

```
没有先失败的测试，就不能写生产代码
```

先写了代码再写测试？删掉它。重新开始。

**没有例外:**
- 不要保留它作为「参考」
- 不要在写测试时「改编」它
- 不要看它
- 删除就是删除

从测试重新实现。句号。

## 测试层次与选择

在编写测试之前，先确定测试类型：

### 单元测试
- **何时使用**: 逻辑验证、算法实现、独立函数、数据转换
- **特征**: 快速、无外部依赖、隔离
- **示例**: retry操作、数据格式转换、业务逻辑

### 集成测试
- **何时使用**: 组件交互、配置生效、外部依赖、网络/数据库
- **特征**: 真实依赖、验证运行时行为
- **示例**: MCP SSE连接、API调用、数据库操作、配置验证

### 端到端测试 (E2E)
- **何时使用**: 完整用户流程、跨多个组件、Docker部署验证
- **特征**: 最接近真实使用、最慢、维护成本高
- **示例**: 完整用户注册流程、Docker容器部署

### 测试类型决策树

```
问题类型分析
├─ 纯逻辑/算法 → 单元测试
├─ 配置问题 → 集成测试（验证生效）
├─ 组件交互 → 集成测试
├─ 完整流程 → 端到端测试
└─ Docker/网络问题 → 集成测试（真实环境）
```

**关键原则**: 对于配置和外部依赖问题，必须测试**运行时行为**，而不仅仅是代码配置。

```python
# ❌ 错误：只测试配置（静态检查）
def test_has_transport_security_config():
    assert 'TransportSecuritySettings' in code

# ✅ 正确：测试运行时行为（集成测试）
def test_sse_rejects_invalid_host():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8001/sse",
            headers={"Host": "invalid-host"}
        )
        assert response.status_code == 421
```

## Red-Green-Refactor 循环

### RED - 编写失败的测试

编写一个最小测试，展示应该发生什么。

**好的测试:**
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'
    
    result = retry_operation(operation)
    
    assert result == 'success'
    assert attempts == 3
```

**集成测试示例（配置/网络问题）:**
```python
@pytest.mark.asyncio
async def test_mcp_sse_accepts_invalid_host_when_dns_rebinding_disabled():
    """测试禁用DNS rebinding protection后，无效Host header也能连接"""
    mcp = FastMCP(
        "TestServer",
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=False
        )
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8001/sse",
            headers={"Host": "192.168.x.x:8001"}
        )
        assert response.status_code == 200
```

清晰的名称，测试真实行为，只测一件事

**要求:**
- 只测一个行为
- 清晰的名称
- 使用真实代码（除非不可避免才用 mock）
- **对于配置/外部依赖问题，必须测试运行时行为**

### 验证 RED - 看它失败

**必须执行。永不跳过。**

确认:
- 测试失败（不是报错）
- 失败信息符合预期
- 因为功能缺失而失败（不是拼写错误）

**测试通过了？** 你在测试已有行为。修复测试。

**测试报错了？** 修复错误，重新运行直到它正确地失败。

### GREEN - 最小代码

编写最简单的代码让测试通过。

不要添加功能、重构其他代码，或「改进」超出测试范围。

### 验证 GREEN - 看它通过

**必须执行。**

确认:
- 测试通过
- 其他测试仍然通过
- 输出干净（没有错误、警告）

**测试失败了？** 修复代码，不是测试。

**其他测试失败了？** 立即修复。

### REFACTOR - 清理

只在 green 之后:
- 移除重复
- 改进命名
- 提取辅助函数

保持测试绿色。不要添加行为。

### 重复

为下一个功能编写下一个失败的测试。

## 常见借口

| 借口 | 现实 |
|------|------|
| 「太简单不需要测试」 | 简单代码也会出错。测试只要30秒。 |
| 「我之后写测试」 | 立即通过的测试什么也不证明。 |
| 「先写后写测试目标一样」 | 后写测试 = 「这做了什么？」先写测试 = 「这应该做什么？」 |
| 「保留作为参考」 | 你会改编它。那就是后写测试。删除就是删除。 |
| 「TDD 会拖慢我」 | TDD 比调试快。务实 = 先测试。 |
| 「集成测试太复杂」 | 配置问题不测试运行时行为，等于没测试。花1小时写集成测试比花1天调试Docker问题值得。 |
| 「静态检查就够了」 | 静态检查只能验证"有没有配置"，不能验证"配置是否生效"。对于配置/网络问题，必须测试运行时行为。 |

## 红线 - 停下来重新开始

- 先写代码再写测试
- 实现后才写测试
- 测试立即通过
- 无法解释为什么测试失败
- 测试「稍后」添加
- 为「就这一次」找借口
- 「这个不同因为...」

**所有这些意味着: 删除代码。用 TDD 重新开始。**

## 外部依赖处理策略

### Docker/容器环境
- **集成测试**: 使用testcontainers或真实容器
- **环境变量**: 通过pytest fixture设置测试环境
- **端口映射**: 测试实际网络行为，不mock网络层

```python
# 示例：测试Docker中的MCP服务
@pytest.fixture
async def mcp_server():
    """启动真实的MCP服务器"""
    process = await asyncio.create_subprocess_exec(
        "python", "-m", "mcp", "run", "main.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await asyncio.sleep(1)  # 等待启动
    yield process
    process.terminate()
    await process.wait()
```

### 网络/HTTP请求
- **真实请求**: 使用httpx/aiohttp发送真实HTTP请求
- **测试服务器**: 使用pytest-asyncio或asgi-lifespan启动测试服务器
- **避免mock**: 除非测试外部不可控的服务

```python
# 示例：测试HTTP API
@pytest.mark.asyncio
async def test_api_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/users")
        assert response.status_code == 200
        assert len(response.json()) > 0
```

### 数据库
- **测试数据库**: 使用内存数据库或测试数据库实例
- **事务回滚**: 每个测试独立，自动回滚
- **fixture复用**: 共享数据库连接

```python
# 示例：测试数据库操作
@pytest.fixture
async def db_session():
    async with async_session() as session:
        async with session.begin():
            yield session
        await session.rollback()
```

### Mock使用原则
- **何时使用**: 外部不可控服务（如第三方API）、硬件依赖
- **何时不使用**: 自己的代码、数据库、Docker环境
- **优先真实**: 优先使用真实环境，除非真的不可控

## 嵌入式领域注意事项

**硬件相关测试:**
- 使用模拟器或 mock 硬件接口
- 优先测试逻辑层，隔离硬件层
- 硬件在环测试作为集成测试

**资源受限环境:**
- 在主机上运行单元测试
- 使用交叉编译验证目标平台兼容性
