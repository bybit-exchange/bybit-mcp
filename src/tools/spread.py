from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post, _public_get


@mcp.tool()
def get_spread_instruments(symbol: str = "", limit: int = 50) -> Any:
    """
    Get spread trading instruments info.

    Args:
        symbol: Spread symbol (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _public_get("/v5/spread/instrument", params)


@mcp.tool()
def get_spread_orderbook(symbol: str, limit: int = 25) -> Any:
    """
    Get spread trading orderbook.

    Args:
        symbol: Spread symbol.
        limit: Depth limit (default: 25).
    """
    return _public_get("/v5/spread/orderbook", {"symbol": symbol, "limit": str(limit)})


@mcp.tool()
def get_spread_recent_trades(symbol: str, limit: int = 50) -> Any:
    """
    Get spread trading recent public trades.

    Args:
        symbol: Spread symbol.
        limit: Number of records (default: 50).
    """
    return _public_get("/v5/spread/recent-trade", {"symbol": symbol, "limit": str(limit)})


@mcp.tool()
def get_spread_tickers(symbol: str) -> Any:
    """
    Get spread trading tickers.

    Args:
        symbol: Spread symbol.
    """
    return _public_get("/v5/spread/tickers", {"symbol": symbol})


@mcp.tool()
def create_spread_order(symbol: str, side: str, order_type: str, qty: str, price: str = "", order_link_id: str = "") -> Any:
    """
    Create a spread trading order.

    Args:
        symbol: Spread symbol.
        side: Buy or Sell.
        order_type: Order type: Limit, Market.
        qty: Order quantity.
        price: Order price (required for Limit orders).
        order_link_id: Unique order link ID (optional).
    """
    params: dict[str, str] = {
        "symbol": symbol, "side": side, "orderType": order_type, "qty": qty,
    }
    if price:
        params["price"] = price
    if order_link_id:
        params["orderLinkId"] = order_link_id
    return _signed_post("/v5/spread/order/create", params)


@mcp.tool()
def amend_spread_order(symbol: str, order_id: str = "", order_link_id: str = "", qty: str = "", price: str = "") -> Any:
    """
    Amend a spread trading order.

    Args:
        symbol: Spread symbol.
        order_id: Order ID (either order_id or order_link_id required).
        order_link_id: Order link ID.
        qty: New quantity (optional).
        price: New price (optional).
    """
    params: dict[str, str] = {"symbol": symbol}
    if order_id:
        params["orderId"] = order_id
    if order_link_id:
        params["orderLinkId"] = order_link_id
    if qty:
        params["qty"] = qty
    if price:
        params["price"] = price
    return _signed_post("/v5/spread/order/amend", params)


@mcp.tool()
def cancel_spread_order(order_id: str = "", order_link_id: str = "") -> Any:
    """
    Cancel a spread trading order.

    Args:
        order_id: Order ID (either order_id or order_link_id required).
        order_link_id: Order link ID.
    """
    params: dict[str, str] = {}
    if order_id:
        params["orderId"] = order_id
    if order_link_id:
        params["orderLinkId"] = order_link_id
    return _signed_post("/v5/spread/order/cancel", params)


@mcp.tool()
def cancel_all_spread_orders(symbol: str = "") -> Any:
    """
    Cancel all spread trading orders.

    Args:
        symbol: Filter by spread symbol (optional).
    """
    params: dict[str, str] = {}
    if symbol:
        params["symbol"] = symbol
    return _signed_post("/v5/spread/order/cancel-all", params)


@mcp.tool()
def get_spread_open_orders(symbol: str = "", limit: int = 50) -> Any:
    """
    Get spread trading open orders.

    Args:
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/spread/order/realtime", params)


@mcp.tool()
def get_spread_order_history(symbol: str = "", limit: int = 50) -> Any:
    """
    Get spread trading order history.

    Args:
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/spread/order/history", params)


@mcp.tool()
def get_spread_trade_history(symbol: str = "", limit: int = 50) -> Any:
    """
    Get spread trading execution history.

    Args:
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/spread/execution/list", params)
