from typing import Any

from src import mcp
from src.client import _signed_get


@mcp.tool()
def get_pre_upgrade_closed_pnl(category: str, symbol: str, limit: int = 50) -> Any:
    """
    Get pre-upgrade closed PnL records.

    Args:
        category: Product type: linear, inverse.
        symbol: The trading pair, e.g., BTCUSDT.
        limit: Number of records (default: 50, max: 100).
    """
    return _signed_get("/v5/pre-upgrade/position/closed-pnl", {
        "category": category, "symbol": symbol, "limit": str(limit),
    })


@mcp.tool()
def get_pre_upgrade_delivery_record(category: str = "option", symbol: str = "", limit: int = 20) -> Any:
    """
    Get pre-upgrade delivery record.

    Args:
        category: Product type: option.
        symbol: Symbol name (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/pre-upgrade/asset/delivery-record", params)


@mcp.tool()
def get_pre_upgrade_trade_history(category: str, symbol: str = "", limit: int = 50) -> Any:
    """
    Get pre-upgrade trade history (execution list).

    Args:
        category: Product type: linear, inverse, option, spot.
        symbol: Symbol name (optional).
        limit: Number of records (default: 50, max: 100).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/pre-upgrade/execution/list", params)


@mcp.tool()
def get_pre_upgrade_order_history(category: str, symbol: str = "", limit: int = 20) -> Any:
    """
    Get pre-upgrade order history.

    Args:
        category: Product type: linear, inverse, option, spot.
        symbol: Symbol name (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/pre-upgrade/order/history", params)


@mcp.tool()
def get_pre_upgrade_settlement(category: str = "linear", symbol: str = "", limit: int = 20) -> Any:
    """
    Get pre-upgrade USDC session settlement record.

    Args:
        category: Product type: linear.
        symbol: Symbol name (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/pre-upgrade/asset/settlement-record", params)


@mcp.tool()
def get_pre_upgrade_transaction_log(category: str, limit: int = 20) -> Any:
    """
    Get pre-upgrade transaction log.

    Args:
        category: Product type: linear, option.
        limit: Number of records (default: 20, max: 50).
    """
    return _signed_get("/v5/pre-upgrade/account/transaction-log", {
        "category": category, "limit": str(limit),
    })
