from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post, _public_get


@mcp.tool()
def get_spot_margin_coin_state(currency: str = "") -> Any:
    """
    Get spot margin coin borrowing state.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/spot-margin-trade/coinstate", params)


@mcp.tool()
def get_spot_margin_auto_repay_mode(currency: str = "") -> Any:
    """
    Get spot margin auto repay mode.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/spot-margin-trade/get-auto-repay-mode", params)


@mcp.tool()
def get_spot_margin_interest_rate_history(currency: str) -> Any:
    """
    Get spot margin historical interest rate.

    Args:
        currency: Currency, e.g., USDT.
    """
    return _signed_get("/v5/spot-margin-trade/interest-rate-history", {"currency": currency})


@mcp.tool()
def get_spot_margin_max_borrowable(currency: str) -> Any:
    """
    Get spot margin max borrowable amount.

    Args:
        currency: Currency, e.g., USDT.
    """
    return _signed_get("/v5/spot-margin-trade/max-borrowable", {"currency": currency})


@mcp.tool()
def get_spot_margin_position_tiers(currency: str = "") -> Any:
    """
    Get spot margin position tiers.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _public_get("/v5/spot-margin-trade/position-tiers", params)


@mcp.tool()
def get_spot_margin_repayment_available(currency: str) -> Any:
    """
    Get available amount to repay for spot margin.

    Args:
        currency: Currency, e.g., USDT.
    """
    return _signed_get("/v5/spot-margin-trade/repayment-available-amount", {"currency": currency})


@mcp.tool()
def set_spot_margin_auto_repay_mode(auto_repay_mode: str, currency: str = "") -> Any:
    """
    Set spot margin auto repay mode.

    Args:
        auto_repay_mode: Auto repay mode: on, off.
        currency: Currency (optional).
    """
    params: dict[str, str] = {"autoRepayMode": auto_repay_mode}
    if currency:
        params["currency"] = currency
    return _signed_post("/v5/spot-margin-trade/set-auto-repay-mode", params)


@mcp.tool()
def set_spot_margin_leverage(leverage: str, currency: str = "") -> Any:
    """
    Set spot margin leverage.

    Args:
        leverage: Leverage value, e.g., "2".
        currency: Currency (optional).
    """
    params: dict[str, str] = {"leverage": leverage}
    if currency:
        params["currency"] = currency
    return _signed_post("/v5/spot-margin-trade/set-leverage", params)


@mcp.tool()
def get_spot_margin_status() -> Any:
    """Get spot margin trading status and leverage info."""
    return _signed_get("/v5/spot-margin-trade/state", {})


@mcp.tool()
def toggle_spot_margin_trade(spot_margin_mode: str) -> Any:
    """
    Toggle spot margin trading on or off.

    Args:
        spot_margin_mode: "1" to enable, "0" to disable.
    """
    return _signed_post("/v5/spot-margin-trade/switch-mode", {"spotMarginMode": spot_margin_mode})


@mcp.tool()
def get_spot_margin_collateral_ratio(currency: str = "") -> Any:
    """
    Get tiered collateral ratio for spot margin.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _public_get("/v5/spot-margin-trade/collateral", params)


@mcp.tool()
def get_spot_margin_vip_data(currency: str = "") -> Any:
    """
    Get VIP margin data (borrow rates, limits).

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _public_get("/v5/spot-margin-trade/data", params)
