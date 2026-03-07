from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def get_positions(symbol: str = "", category: str = "linear") -> Any:
    """
    Get current positions for derivatives.

    Args:
        symbol: The trading pair (optional, returns all if empty).
        category: Product type: linear, inverse (default: linear).

    Returns:
        List of current positions.
    """
    params = {"category": category}
    if symbol:
        params["symbol"] = symbol
    result = _signed_get("/v5/position/list", params)
    if "error" in result:
        return result
    return [
        {
            "symbol": pos.get("symbol", ""),
            "side": pos.get("side", ""),
            "size": pos.get("size", ""),
            "avgPrice": pos.get("avgPrice", ""),
            "unrealisedPnl": pos.get("unrealisedPnl", ""),
            "leverage": pos.get("leverage", ""),
            "liqPrice": pos.get("liqPrice", ""),
        }
        for pos in result.get("list", [])
    ]


@mcp.tool()
def set_leverage(symbol: str, buy_leverage: str, sell_leverage: str, category: str = "linear") -> Any:
    """
    Set leverage for a symbol.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        buy_leverage: Buy side leverage, e.g., "10".
        sell_leverage: Sell side leverage, e.g., "10".
        category: Product type: linear, inverse (default: linear).

    Returns:
        Leverage setting result.
    """
    result = _signed_post("/v5/position/set-leverage", {
        "category": category,
        "symbol": symbol,
        "buyLeverage": buy_leverage,
        "sellLeverage": sell_leverage,
    })
    if "error" in result:
        return result
    return {"message": f"Leverage set to {buy_leverage}x/{sell_leverage}x for {symbol}"}


@mcp.tool()
def set_trading_stop(
    symbol: str,
    category: str = "linear",
    take_profit: str = "",
    stop_loss: str = "",
    position_idx: int = 0,
) -> Any:
    """
    Set take profit and/or stop loss for a position.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: linear, inverse (default: linear).
        take_profit: Take profit price. Leave empty to not set.
        stop_loss: Stop loss price. Leave empty to not set.
        position_idx: Position index: 0 (one-way), 1 (buy side), 2 (sell side). Default: 0.

    Returns:
        Trading stop setting result.
    """
    params: dict[str, Any] = {
        "category": category,
        "symbol": symbol,
        "positionIdx": position_idx,
    }
    if take_profit:
        params["takeProfit"] = take_profit
    if stop_loss:
        params["stopLoss"] = stop_loss
    result = _signed_post("/v5/position/trading-stop", params)
    if "error" in result:
        return result
    return {"message": f"Trading stop set for {symbol}"}


@mcp.tool()
def switch_position_mode(symbol: str, mode: int, category: str = "linear", coin: str = "") -> Any:
    """
    Switch position mode between one-way and hedge mode.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        mode: Position mode: 0 (merged single side), 3 (both sides).
        category: Product type: linear, inverse (default: linear).
        coin: Required for inverse. Coin name, e.g., BTC.

    Returns:
        Position mode switch result.
    """
    params: dict[str, Any] = {
        "category": category,
        "symbol": symbol,
        "mode": mode,
    }
    if coin:
        params["coin"] = coin
    result = _signed_post("/v5/position/switch-mode", params)
    if "error" in result:
        return result
    mode_name = "one-way" if mode == 0 else "hedge"
    return {"message": f"Position mode switched to {mode_name} for {symbol}"}


@mcp.tool()
def get_closed_pnl(
    symbol: str,
    category: str = "linear",
    limit: int = 50,
) -> Any:
    """
    Get closed profit and loss records.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: linear, inverse (default: linear).
        limit: Number of records (default: 50, max: 100).

    Returns:
        List of closed PnL records.
    """
    result = _signed_get("/v5/position/closed-pnl", {
        "category": category,
        "symbol": symbol,
        "limit": str(limit),
    })
    if "error" in result:
        return result
    return [
        {
            "symbol": pnl.get("symbol", ""),
            "side": pnl.get("side", ""),
            "qty": pnl.get("qty", ""),
            "entryPrice": pnl.get("avgEntryPrice", ""),
            "exitPrice": pnl.get("avgExitPrice", ""),
            "closedPnl": pnl.get("closedPnl", ""),
            "createdTime": pnl.get("createdTime", ""),
            "updatedTime": pnl.get("updatedTime", ""),
        }
        for pnl in result.get("list", [])
    ]


@mcp.tool()
def set_auto_add_margin(symbol: str, auto_add_margin: int, category: str = "linear", position_idx: int = 0) -> Any:
    """
    Set auto add margin for a position.

    Args:
        symbol: Symbol, e.g., BTCUSDT.
        auto_add_margin: 0: off, 1: on.
        category: Product type: linear (default: linear).
        position_idx: 0: one-way, 1: hedge-Buy, 2: hedge-Sell (default: 0).
    """
    return _signed_post("/v5/position/set-auto-add-margin", {
        "category": category, "symbol": symbol,
        "autoAddMargin": auto_add_margin, "positionIdx": position_idx,
    })


@mcp.tool()
def get_closed_options_positions(symbol: str = "", limit: int = 50) -> Any:
    """
    Get closed options positions.

    Args:
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 50, max: 100).
    """
    params: dict[str, str] = {"category": "option", "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/position/get-closed-positions", params)


@mcp.tool()
def confirm_risk_limit(category: str, symbol: str) -> Any:
    """
    Confirm new risk limit (required after risk limit change that triggers margin adjustment).

    Args:
        category: Product type: linear, inverse.
        symbol: Symbol, e.g., BTCUSDT.
    """
    return _signed_post("/v5/position/confirm-pending-mmr", {
        "category": category, "symbol": symbol,
    })


@mcp.tool()
def add_reduce_margin(category: str, symbol: str, margin: str, position_idx: int = 0) -> Any:
    """
    Add or reduce margin for a position (isolated margin mode).

    Args:
        category: Product type: linear, inverse.
        symbol: Symbol, e.g., BTCUSDT.
        margin: Positive to add (e.g., "10"), negative to reduce (e.g., "-10").
        position_idx: 0: one-way, 1: hedge-Buy, 2: hedge-Sell (default: 0).
    """
    return _signed_post("/v5/position/add-margin", {
        "category": category, "symbol": symbol,
        "margin": margin, "positionIdx": position_idx,
    })


@mcp.tool()
def move_position(from_uid: str, to_uid: str, legs: list[dict]) -> Any:
    """
    Move positions between UIDs (master API key only).

    Args:
        from_uid: Source UID.
        to_uid: Destination UID.
        legs: List of position legs, each with: category, symbol, price, side, qty.
              Max 25 legs per request.
    """
    return _signed_post("/v5/position/move-positions", {
        "fromUid": from_uid, "toUid": to_uid, "list": legs,
    })


@mcp.tool()
def get_move_position_history(category: str = "", symbol: str = "", limit: int = 20) -> Any:
    """
    Get move position history.

    Args:
        category: Product type: linear, inverse, spot, option (optional).
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 20, max: 200).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if category:
        params["category"] = category
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/position/move-history", params)
