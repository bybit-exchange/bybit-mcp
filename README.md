<div align="center">

# 🟡 Bybit MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)
[![Tools](https://img.shields.io/badge/Tools-246-orange.svg)](#-available-tools-246)
[![Bybit V5 API](https://img.shields.io/badge/Bybit-V5%20API-green.svg)](https://bybit-exchange.github.io/docs/v5/intro)

**The most comprehensive MCP server for Bybit — 246 tools covering the entire Bybit V5 API**

[Quick Start](#-quick-start) •
[Features](#-features) •
[Configuration](#%EF%B8%8F-configuration) •
[Tools Reference](#-available-tools-246) •
[Contributing](#-contributing)

</div>

---

## 🎯 Overview

Bybit MCP Server enables AI assistants like **Claude**, **Cursor**, **ChatGPT**, and other MCP-compatible clients to interact directly with the Bybit cryptocurrency exchange. Execute trades, manage portfolios, analyze markets, and automate strategies — all through natural language.

### Why Bybit MCP?

- **🔥 Complete Coverage** — 246 tools spanning every Bybit V5 API endpoint
- **🔐 Secure by Design** — API credentials never leave your machine
- **👁️ Read-Only Mode** — Use all market tools without any API key
- **📡 Triple Transport** — STDIO, SSE, and Streamable HTTP
- **🔌 Universal Compatibility** — Works with Claude Desktop, Cursor, ChatGPT, and any MCP client
- **⚡ Zero Config Start** — Just `uv run bybit.py` and go

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📈 Trading & Markets
- **Spot Trading** — Market & limit orders, batch operations
- **Derivatives** — Linear & inverse perpetuals
- **Order Management** — Amend, cancel, batch, DCP
- **Market Data** — Klines, orderbook, tickers, funding rates
- **Open Interest** — Long/short ratio, ADL alerts

</td>
<td width="50%">

### 💰 Earn & Lending
- **Simple Earn** — Stake, redeem, yield tracking
- **Crypto Loans** — Old & new (fixed + flexible)
- **Leveraged Tokens** — Subscribe & redeem
- **Spot Margin** — Cross-margin trading
- **OTC Lending** — Institutional loan management

</td>
</tr>
<tr>
<td width="50%">

### 🏦 Account & Assets
- **Wallet** — Deposits, withdrawals, transfers
- **Multi-Account** — Sub-accounts, universal transfers
- **Asset Convert** — Crypto-to-crypto, small balance, fiat
- **Margin Modes** — Cross, isolated, portfolio margin
- **Risk Management** — MMP, leverage, TP/SL

</td>
<td width="50%">

### 🛠️ Advanced
- **Spread Trading** — Spread instruments & orders
- **Block Trading (RFQ)** — Request for quote workflow
- **Broker** — Earnings, rate limits, vouchers
- **Strategy** — Built-in arbitrage detection
- **Announcements** — Exchange news & system status

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Python ≥ 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- Bybit account with API credentials *(optional — market data works without)*

### Installation

```bash
# Clone the repository
git clone https://github.com/JohnnyWic/bybit-mcp.git
cd bybit-mcp

# Install dependencies
uv sync
```

### Run

```bash
# Start in STDIO mode (default)
uv run bybit.py

# Start in SSE mode
uv run bybit.py --transport sse --port 8000

# Start in Streamable HTTP mode
uv run bybit.py --transport streamable-http --port 8000
```

> 💡 **No API key?** No problem! All 23 market tools work without authentication.

---

## ⚙️ Configuration

### Environment Variables (Recommended)

```bash
cp .env.example .env
```

```env
BYBIT_API_KEY=your_api_key_here
BYBIT_SECRET_KEY=your_secret_key_here
BYBIT_TESTNET=false
```

> **🔒 Security Note:** Never commit your `.env` file. It's already in `.gitignore`.

### Command Line Arguments

```bash
uv run bybit.py --bybit-api-key YOUR_KEY --bybit-secret-key YOUR_SECRET
```

### Keyless Read-Only Mode

Simply start without any credentials. All market data tools (prices, klines, orderbook, funding rates, etc.) work normally. Authenticated endpoints return a clear error message.

### Structured Logging

```bash
uv run bybit.py --log-level DEBUG    # DEBUG / INFO / WARNING / ERROR
```

---

## 🖥️ Client Configuration

### Claude Desktop / Cursor (STDIO)

Add to your MCP config file (e.g., `~/.cursor/mcp.json`):

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

With inline credentials:

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/bybit-mcp", "run", "bybit.py",
        "--bybit-api-key", "YOUR_API_KEY",
        "--bybit-secret-key", "YOUR_SECRET_KEY"
      ]
    }
  }
}
```

### ChatGPT / Web Apps (SSE)

1. Start the server: `uv run bybit.py --transport sse --port 8000`
2. Configure client:

```json
{
  "mcpServers": {
    "bybit-mcp": {
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```

---

## 💬 Usage Examples

### Check Market Price

```
"What's the current price of BTC?"
```

### Place a Trade

```
"Buy 0.01 BTC at market price on spot"
```

### Analyze Funding Rates

```
"Show me the funding rate history for ETHUSDT over the last 24 hours"
```

### Manage Positions

```
"What are my open positions? Set a stop loss at 95000 for my BTCUSDT long"
```

### Portfolio Overview

```
"Show my unified account balance and all open orders"
```

---

## 📊 Available Tools (246)

| Module | Tools | Description |
|--------|------:|-------------|
| **Market** | 23 | Prices, klines, orderbook, funding rates, open interest, tickers *(no API key needed)* |
| **Trade** | 15 | Market/limit orders, amend, cancel, batch operations, DCP |
| **Account** | 25 | Balance, fee rates, margin mode, collateral, MMP, transaction log |
| **Position** | 11 | Positions, leverage, TP/SL, auto-margin, move positions |
| **Asset** | 41 | Deposits, withdrawals, transfers, convert, fiat, address management |
| **Lending** | 39 | Crypto loans — legacy + new (fixed & flexible) |
| **User** | 15 | Sub-accounts, API key management, affiliate |
| **RFQ** | 15 | Block trading — create/cancel RFQ, quotes, executions |
| **Spot Margin** | 12 | Spot margin trading, borrow, repay, collateral |
| **Spread** | 11 | Spread instruments, orderbook, trading |
| **Broker** | 10 | Broker earnings, rate limits, vouchers |
| **OTC** | 7 | Institutional OTC lending |
| **Pre-Upgrade** | 6 | Pre-upgrade historical data queries |
| **Earn** | 6 | Staking, redemption, yield tracking |
| **Leveraged Token** | 5 | Leveraged token subscribe/redeem |
| **Announcement** | 2 | Exchange announcements, system status |
| **Strategy** | 2 | Built-in arbitrage pair detection |

**Total: 246 tools**

<details>
<summary><b>📋 View all tool names</b></summary>

```bash
uv run python -c "
import src.tools
from src import mcp
for name in sorted(mcp._tool_manager._tools):
    print(name)
"
```

</details>

---

## 🏗️ Project Structure

```
bybit-mcp/
├── bybit.py                    # Entry point (backward compatible)
├── src/
│   ├── __init__.py             # Shared FastMCP instance
│   ├── main.py                 # CLI: dotenv + argparse + logging + mcp.run()
│   ├── client.py               # Config singleton + HMAC signing + HTTP methods
│   └── tools/
│       ├── __init__.py         # Auto-imports all tool modules
│       ├── market.py           # 23 tools — public market data
│       ├── trade.py            # 15 tools — order management
│       ├── account.py          # 25 tools — account operations
│       ├── position.py         # 11 tools — position management
│       ├── asset.py            # 41 tools — wallet & transfers
│       ├── lending.py          # 39 tools — crypto loans
│       ├── earn.py             #  6 tools — staking & yield
│       ├── leveraged_token.py  #  5 tools — leveraged tokens
│       ├── spot_margin.py      # 12 tools — spot margin
│       ├── user.py             # 15 tools — sub-accounts & API keys
│       ├── broker.py           # 10 tools — broker services
│       ├── otc.py              #  7 tools — OTC lending
│       ├── spread.py           # 11 tools — spread trading
│       ├── rfq.py              # 15 tools — block trading RFQ
│       ├── pre_upgrade.py      #  6 tools — pre-upgrade data
│       ├── announcement.py     #  2 tools — announcements
│       └── strategy.py         #  2 tools — arbitrage strategies
├── .env.example                # Environment variable template
├── pyproject.toml              # Project config & dependencies
└── LICENSE                     # MIT License
```

---

## ⚠️ Disclaimer

This software is provided for educational and informational purposes only.

- **Not Financial Advice** — This tool does not provide financial, investment, or trading advice
- **Use at Your Own Risk** — Cryptocurrency trading involves substantial risk of loss
- **API Security** — Protect your API credentials; use IP restrictions and disable withdrawal permissions
- **Test First** — Always test on [Bybit Testnet](https://testnet.bybit.com/) before using real funds (`--testnet` flag)
- **No Warranty** — The software is provided "as is" without warranty of any kind

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Tools

1. Add your tool function in the appropriate `src/tools/*.py` module
2. Decorate with `@mcp.tool()`
3. Use `_public_get` for unauthenticated or `_signed_get`/`_signed_post` for authenticated endpoints
4. That's it — tools are auto-registered on import

---

## 📚 Resources

| Resource | Description |
|----------|-------------|
| [Bybit V5 API Docs](https://bybit-exchange.github.io/docs/v5/intro) | Official Bybit API documentation |
| [Bybit Testnet](https://testnet.bybit.com/) | Practice trading with test funds |
| [MCP Specification](https://modelcontextprotocol.io/) | Model Context Protocol spec |
| [uv Package Manager](https://docs.astral.sh/uv/) | Fast Python package manager |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for the Bybit trading community**

</div>
