from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def place_market_order(symbol: str, side: str, qty: str, category: str = "spot") -> Any:
    """
    Place a market order to buy or sell.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        side: Buy or Sell.
        qty: Amount to trade.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        Order placement result.
    """
    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": "Market",
        "qty": qty,
    }
    result = _signed_post("/v5/order/create", params)
    if "error" in result:
        return result
    return {
        "message": f"{side} {qty} {symbol} market order placed",
        "orderId": result.get("orderId", ""),
        "orderLinkId": result.get("orderLinkId", ""),
    }


@mcp.tool()
def place_limit_order(symbol: str, side: str, qty: str, price: str, category: str = "spot") -> Any:
    """
    Place a limit order to buy or sell.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        side: Buy or Sell.
        qty: Amount to trade.
        price: Limit price.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        Order placement result.
    """
    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": "Limit",
        "qty": qty,
        "price": price,
    }
    result = _signed_post("/v5/order/create", params)
    if "error" in result:
        return result
    return {
        "message": f"{side} {qty} {symbol} limit order placed at {price}",
        "orderId": result.get("orderId", ""),
        "orderLinkId": result.get("orderLinkId", ""),
    }


@mcp.tool()
def get_trade_history(symbol: str, category: str = "spot", limit: int = 20) -> Any:
    """
    Get recent trade history for a pair.

    Args:
        symbol: The trading pair.
        category: Product type: spot, linear, inverse (default: spot).
        limit: Number of trades to fetch (default: 20, max: 100).

    Returns:
        List of trade summaries.
    """
    result = _signed_get("/v5/execution/list", {
        "category": category,
        "symbol": symbol,
        "limit": str(limit),
    })
    if "error" in result:
        return result
    return [
        {
            "time": trade.get("execTime", ""),
            "side": trade.get("side", ""),
            "qty": trade.get("execQty", ""),
            "price": trade.get("execPrice", ""),
            "fee": trade.get("execFee", ""),
            "orderId": trade.get("orderId", ""),
        }
        for trade in result.get("list", [])
    ]


@mcp.tool()
def get_open_orders(symbol: str, category: str = "spot") -> Any:
    """
    Get open orders for a symbol.

    Args:
        symbol: The trading pair.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        List of open orders.
    """
    result = _signed_get("/v5/order/realtime", {
        "category": category,
        "symbol": symbol,
    })
    if "error" in result:
        return result
    return [
        {
            "orderId": order.get("orderId", ""),
            "side": order.get("side", ""),
            "orderType": order.get("orderType", ""),
            "qty": order.get("qty", ""),
            "price": order.get("price", ""),
            "status": order.get("orderStatus", ""),
            "createdTime": order.get("createdTime", ""),
        }
        for order in result.get("list", [])
    ]


@mcp.tool()
def cancel_order(symbol: str, order_id: str, category: str = "spot") -> Any:
    """
    Cancel a specific order.

    Args:
        symbol: The trading pair.
        order_id: Order ID to cancel.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        Cancellation result.
    """
    result = _signed_post("/v5/order/cancel", {
        "category": category,
        "symbol": symbol,
        "orderId": order_id,
    })
    if "error" in result:
        return result
    return {"message": f"Order {order_id} canceled", "orderId": result.get("orderId", "")}


@mcp.tool()
def cancel_all_orders(symbol: str, category: str = "spot") -> Any:
    """
    Cancel all open orders for a symbol.

    Args:
        symbol: The trading pair.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        Cancellation result.
    """
    result = _signed_post("/v5/order/cancel-all", {
        "category": category,
        "symbol": symbol,
    })
    if "error" in result:
        return result
    return {"message": f"All orders for {symbol} canceled", "result": result}


@mcp.tool()
def amend_order(
    symbol: str,
    order_id: str,
    category: str = "spot",
    qty: str = "",
    price: str = "",
) -> Any:
    """
    Amend (modify) an existing open order.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        order_id: Order ID to amend.
        category: Product type: spot, linear, inverse (default: spot).
        qty: New quantity (optional, leave empty to keep unchanged).
        price: New price (optional, leave empty to keep unchanged).

    Returns:
        Amendment result.
    """
    params: dict[str, str] = {
        "category": category,
        "symbol": symbol,
        "orderId": order_id,
    }
    if qty:
        params["qty"] = qty
    if price:
        params["price"] = price
    result = _signed_post("/v5/order/amend", params)
    if "error" in result:
        return result
    return {
        "message": f"Order {order_id} amended",
        "orderId": result.get("orderId", ""),
    }


@mcp.tool()
def get_order_history(
    symbol: str,
    category: str = "spot",
    limit: int = 50,
) -> Any:
    """
    Get historical (closed/cancelled/filled) orders.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse (default: spot).
        limit: Number of records (default: 50, max: 50).

    Returns:
        List of historical orders.
    """
    result = _signed_get("/v5/order/history", {
        "category": category,
        "symbol": symbol,
        "limit": str(limit),
    })
    if "error" in result:
        return result
    return [
        {
            "orderId": order.get("orderId", ""),
            "symbol": order.get("symbol", ""),
            "side": order.get("side", ""),
            "orderType": order.get("orderType", ""),
            "qty": order.get("qty", ""),
            "price": order.get("price", ""),
            "status": order.get("orderStatus", ""),
            "avgPrice": order.get("avgPrice", ""),
            "cumExecQty": order.get("cumExecQty", ""),
            "createdTime": order.get("createdTime", ""),
            "updatedTime": order.get("updatedTime", ""),
        }
        for order in result.get("list", [])
    ]


@mcp.tool()
def batch_place_order(category: str, orders: list[dict[str, str]]) -> Any:
    """
    Place multiple orders in a single request (max 10).

    Args:
        category: Product type: spot, linear, inverse, option.
        orders: List of order dicts. Each must contain: symbol, side, orderType, qty.
                Optional fields: price, timeInForce, orderLinkId, etc.
                Example: [{"symbol": "BTCUSDT", "side": "Buy", "orderType": "Limit", "qty": "0.01", "price": "50000"}]

    Returns:
        Batch order placement results.
    """
    result = _signed_post("/v5/order/create-batch", {
        "category": category,
        "request": orders,
    })
    if "error" in result:
        return result
    return result


@mcp.tool()
def batch_cancel_order(category: str, orders: list[dict[str, str]]) -> Any:
    """
    Cancel multiple orders in a single request (max 10).

    Args:
        category: Product type: spot, linear, inverse, option.
        orders: List of order dicts. Each must contain: symbol and orderId (or orderLinkId).
                Example: [{"symbol": "BTCUSDT", "orderId": "123456"}]

    Returns:
        Batch cancellation results.
    """
    result = _signed_post("/v5/order/cancel-batch", {
        "category": category,
        "request": orders,
    })
    if "error" in result:
        return result
    return result


@mcp.tool()
def batch_amend_order(category: str, orders: list[dict[str, str]]) -> Any:
    """
    Amend multiple orders in a single request (max 20 for derivatives, 10 for spot).

    Args:
        category: Product type: spot, linear, inverse, option.
        orders: List of order dicts. Each must contain: symbol, and either orderId or orderLinkId.
                Optional: qty, price, triggerPrice, takeProfit, stopLoss, etc.

    Returns:
        Batch amendment results.
    """
    result = _signed_post("/v5/order/amend-batch", {
        "category": category,
        "request": orders,
    })
    if "error" in result:
        return result
    return result


@mcp.tool()
def set_dcp(time_window: int, product: str = "OPTIONS") -> Any:
    """
    Set Disconnect Cancel All (DCP) - auto-cancel orders on disconnect.

    Args:
        time_window: Time window in seconds (3-300).
        product: Product type: OPTIONS, DERIVATIVES, SPOT (default: OPTIONS).
    """
    return _signed_post("/v5/order/disconnected-cancel-all", {
        "timeWindow": time_window, "product": product,
    })


@mcp.tool()
def get_open_closed_orders(
    category: str,
    symbol: str = "",
    open_only: int = 0,
    order_filter: str = "",
    limit: int = 20,
) -> Any:
    """
    Get open and/or closed orders (unified endpoint).

    Args:
        category: Product type: linear, inverse, spot, option.
        symbol: Filter by symbol (optional).
        open_only: 0: open orders only (default), 1: recent 500 closed orders.
        order_filter: Filter: Order, StopOrder, tpslOrder, OcoOrder (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    if open_only:
        params["openOnly"] = str(open_only)
    if order_filter:
        params["orderFilter"] = order_filter
    return _signed_get("/v5/order/realtime", params)


@mcp.tool()
def pre_check_order(
    category: str,
    symbol: str,
    side: str,
    order_type: str,
    qty: str,
    price: str = "",
) -> Any:
    """
    Pre-check an order before placing it (validates margin, limits, etc.).

    Args:
        category: Product type: inverse, linear, option.
        symbol: Symbol, e.g., BTCUSDT.
        side: Buy or Sell.
        order_type: Market or Limit.
        qty: Order quantity.
        price: Order price (required for Limit).
    """
    params: dict[str, str] = {
        "category": category, "symbol": symbol, "side": side,
        "orderType": order_type, "qty": qty,
    }
    if price:
        params["price"] = price
    return _signed_post("/v5/order/pre-check", params)


@mcp.tool()
def get_spot_borrow_quota(symbol: str, side: str) -> Any:
    """
    Get spot borrow quota for margin trading.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        side: Buy or Sell.
    """
    return _signed_get("/v5/order/spot-borrow-check", {
        "category": "spot", "symbol": symbol, "side": side,
    })
