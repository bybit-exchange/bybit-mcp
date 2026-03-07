# Bybit MCP Server

基于 MCP (Model Context Protocol) 的 Bybit V5 交易接口服务器。通过 MCP 协议让 AI 助手（如 Cursor、Claude Desktop 等）直接与 Bybit 交易所交互，实现智能交易和市场分析。

## 功能特性

- 获取实时加密货币价格
- 查询账户资产余额
- 下单交易（市价单、限价单）
- 查询交易历史
- 查询当前未完成订单
- 取消订单 / 批量取消订单
- 获取K线数据
- 获取订单簿深度
- 查询持仓信息
- 设置杠杆倍数
- 获取交易对信息
- 获取资金费率历史
- 执行对冲套利策略
- 自动寻找套利机会

支持 Bybit V5 API 的 spot、linear、inverse 等多种产品类型。

## 安装要求

- Python >= 3.13
- mcp[cli] >= 1.6.0
- requests >= 2.32.3

## 安装和配置

1. 克隆仓库：
```bash
git clone https://github.com/JohnnyWic/bybit-mcp.git
cd bybit-mcp
```

2. 安装依赖：
```bash
uv sync
```

3. 配置 MCP：

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

如需使用测试网，添加 `"--testnet"` 到 args 中。

## 可用工具

| 工具 | 说明 |
|------|------|
| `get_symbol_price` | 获取交易对当前价格 |
| `get_account_balance` | 查询账户余额 |
| `place_market_order` | 下市价单 |
| `place_limit_order` | 下限价单 |
| `get_trade_history` | 获取交易历史 |
| `get_open_orders` | 查询未完成订单 |
| `cancel_order` | 取消订单 |
| `cancel_all_orders` | 取消所有订单 |
| `get_kline` | 获取K线数据 |
| `get_orderbook` | 获取订单簿深度 |
| `get_positions` | 查询持仓信息 |
| `set_leverage` | 设置杠杆倍数 |
| `get_instruments_info` | 获取交易对规格信息 |
| `get_funding_rate_history` | 获取资金费率历史 |
| `execute_hedge_arbitrage_strategy` | 执行对冲套利 |
| `find_arbitrage_pairs` | 寻找套利机会 |

## 安全提示

- 妥善保管 API 密钥
- 建议设置 API 权限限制（如仅允许交易，禁止提币）
- 建议先在测试网 (`--testnet`) 上进行测试
- 套利策略存在风险，请谨慎使用

## 许可证

MIT
