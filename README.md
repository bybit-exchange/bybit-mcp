# Bybit MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io)

基于 MCP (Model Context Protocol) 的 Bybit V5 交易接口服务器。通过 MCP 协议让 AI 助手（如 Cursor、Claude Desktop 等）直接与 Bybit 交易所交互，实现智能交易和市场分析。

## 功能特性

- 246 个工具，全量覆盖 Bybit V5 API（行情、交易、账户、持仓、资产、借贷、理财、杠杆代币、现货杠杆、用户管理、经纪商、OTC、Spread、RFQ 等）
- 支持 STDIO、SSE、Streamable HTTP 三种传输模式
- 支持 `.env` 文件配置，也支持命令行参数
- 无密钥只读模式：无需 API key 即可使用所有行情工具
- 结构化日志 (`--log-level DEBUG/INFO/WARNING/ERROR`)
- 模块化架构，易于扩展

## 安装

```bash
git clone https://github.com/JohnnyWic/bybit-mcp.git
cd bybit-mcp
uv sync
```

## 配置

### 方式一：.env 文件（推荐）

复制示例文件并填入你的 API 密钥：

```bash
cp .env.example .env
```

```env
BYBIT_API_KEY=your_api_key_here
BYBIT_SECRET_KEY=your_secret_key_here
BYBIT_TESTNET=false
```

### 方式二：命令行参数

```bash
uv run bybit.py --bybit-api-key YOUR_KEY --bybit-secret-key YOUR_SECRET
```

### 方式三：无密钥只读模式

不配置任何密钥即可启动，行情类工具（价格、K线、订单簿等）正常可用。调用需要认证的工具时会返回清晰的错误提示。

## 启动

### STDIO 模式（默认，用于 MCP 客户端集成）

```bash
uv run bybit.py
```

### SSE 模式

```bash
uv run bybit.py --transport sse --host 127.0.0.1 --port 8000
```

### Streamable HTTP 模式

```bash
uv run bybit.py --transport streamable-http --host 127.0.0.1 --port 8000
```

## MCP 客户端配置

### STDIO 模式

在你的 MCP 配置文件中（如 `~/.cursor/mcp.json`）添加：

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/bybit-mcp",
        "run",
        "bybit.py",
        "--bybit-api-key",
        "YOUR_API_KEY",
        "--bybit-secret-key",
        "YOUR_SECRET_KEY"
      ]
    }
  }
}
```

如使用 `.env` 文件配置密钥，可简化为：

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/bybit-mcp", "run", "bybit.py"]
    }
  }
}
```

### SSE 模式

先启动服务器，然后配置客户端连接：

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

## 可用工具（246 个）

| 模块 | 工具数 | 说明 |
|------|--------|------|
| **Market** (行情) | 23 | 价格、K线、订单簿、资金费率、持仓量等（无需 API key） |
| **Trade** (交易) | 15 | 下单、撤单、改单、批量操作、订单历史 |
| **Account** (账户) | 25 | 余额、手续费、保证金模式、借贷、MMP |
| **Position** (持仓) | 11 | 持仓查询、杠杆、止盈止损、移仓 |
| **Asset** (资产) | 41 | 充提币、划转、兑换、法币、地址管理 |
| **Pre-Upgrade** | 6 | 升级前历史数据查询 |
| **Lending** (借贷) | 39 | 加密借贷（旧版+新版固定/灵活） |
| **Earn** (理财) | 6 | 质押、赎回、收益查询 |
| **Leveraged Token** | 5 | 杠杆代币申购/赎回 |
| **Spot Margin** | 12 | 现货杠杆交易管理 |
| **User** (用户) | 15 | 子账户、API Key 管理 |
| **Broker** (经纪商) | 10 | 经纪商收益、限速、代金券 |
| **OTC** | 7 | 机构借贷 |
| **Spread** | 11 | 价差交易 |
| **RFQ** | 15 | 大宗交易询价 |
| **Announcement** | 2 | 公告、系统状态 |
| **Strategy** (策略) | 2 | 套利策略 |

完整工具列表请运行 `uv run python -c "import src.tools; from src import mcp; [print(n) for n in sorted(mcp._tool_manager._tools)]"` 查看。

## 安全提示

- 妥善保管 API 密钥，勿提交 `.env` 文件到版本控制
- 建议设置 API 权限限制（如仅允许交易，禁止提币）
- 建议先在测试网 (`--testnet`) 上进行测试
- 套利策略存在风险，请谨慎使用

## 许可证

[MIT](LICENSE)
