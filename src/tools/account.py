from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def get_account_balance(coin: str, account_type: str = "UNIFIED") -> Any:
    """
    Get the balance of a specific cryptocurrency asset.

    Args:
        coin: The cryptocurrency symbol, e.g., BTC.
        account_type: Account type: UNIFIED, CONTRACT, SPOT, FUND (default: UNIFIED).

    Returns:
        Asset balance info.
    """
    result = _signed_get("/v5/account/wallet-balance", {"accountType": account_type})
    if "error" in result:
        return result
    accounts = result.get("list", [])
    for account in accounts:
        for c in account.get("coin", []):
            if c["coin"] == coin:
                return {
                    "coin": coin,
                    "available_balance": c.get("availableToWithdraw", "0"),
                    "wallet_balance": c.get("walletBalance", "0"),
                    "equity": c.get("equity", "0"),
                }
    return {"error": f"No balance found for {coin}"}


@mcp.tool()
def get_fee_rate(symbol: str, category: str = "spot") -> Any:
    """
    Get trading fee rate for a symbol.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse, option (default: spot).

    Returns:
        Fee rate information.
    """
    result = _signed_get("/v5/account/fee-rate", {
        "category": category, "symbol": symbol,
    })
    if "error" in result:
        return result
    rates = result.get("list", [])
    if rates:
        return rates[0]
    return {"error": "No fee rate data found"}


@mcp.tool()
def get_account_info() -> Any:
    """
    Get account info including margin mode and account type.

    Returns:
        Account configuration information.
    """
    return _signed_get("/v5/account/info", {})


@mcp.tool()
def get_transaction_log(
    category: str = "spot",
    limit: int = 50,
) -> Any:
    """
    Get transaction logs.

    Args:
        category: Product type: spot, linear, inverse, option (default: spot).
        limit: Number of records (default: 50, max: 50).

    Returns:
        List of transaction log entries.
    """
    result = _signed_get("/v5/account/transaction-log", {
        "category": category, "limit": str(limit),
    })
    if "error" in result:
        return result
    return result.get("list", [])


@mcp.tool()
def batch_set_collateral_coin(request: list[dict]) -> Any:
    """
    Batch set collateral coin on/off.

    Args:
        request: List of objects, each with: coin (string), collateralSwitch ("ON"/"OFF").
    """
    return _signed_post("/v5/account/set-collateral-switch-batch", {"request": request})


@mcp.tool()
def manual_borrow(coin: str, amount: str) -> Any:
    """
    Manually borrow funds in unified margin account.

    Args:
        coin: Coin to borrow, e.g., USDT.
        amount: Borrow amount.
    """
    return _signed_post("/v5/account/borrow", {"coin": coin, "amount": amount})


@mcp.tool()
def get_borrow_history(currency: str = "", limit: int = 20) -> Any:
    """
    Get borrow history.

    Args:
        currency: Filter by currency (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/account/borrow-history", params)


@mcp.tool()
def get_coin_greeks(base_coin: str = "") -> Any:
    """
    Get coin greeks (delta, gamma, vega, theta).

    Args:
        base_coin: Base coin, e.g., BTC (optional).
    """
    params: dict[str, str] = {}
    if base_coin:
        params["baseCoin"] = base_coin
    return _signed_get("/v5/asset/coin-greeks", params)


@mcp.tool()
def get_collateral_info(currency: str = "") -> Any:
    """
    Get collateral coin info (haircut rates, etc.).

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/account/collateral-info", params)


@mcp.tool()
def get_dcp_info() -> Any:
    """Get Disconnect Cancel All (DCP) configuration info."""
    return _signed_get("/v5/account/query-dcp-info", {})


@mcp.tool()
def get_mmp_state(base_coin: str) -> Any:
    """
    Get Market Maker Protection (MMP) state.

    Args:
        base_coin: Base coin, e.g., BTC.
    """
    return _signed_get("/v5/account/mmp-state", {"baseCoin": base_coin})


@mcp.tool()
def get_trade_behaviour_config() -> Any:
    """Get trade behaviour configuration settings."""
    return _signed_get("/v5/account/user-setting-config", {})


@mcp.tool()
def get_account_instruments_info(category: str, symbol: str = "", limit: int = 200) -> Any:
    """
    Get account-level instruments info (tradable instruments for your account).

    Args:
        category: Product type: spot, linear, inverse.
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 200, max: 200).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/account/instruments-info", params)


@mcp.tool()
def manual_repay_no_convert(coin: str, amount: str = "") -> Any:
    """
    Manual repay without asset conversion.

    Args:
        coin: Coin to repay, e.g., USDT.
        amount: Repay amount (optional, repays all if empty).
    """
    params: dict[str, str] = {"coin": coin}
    if amount:
        params["amount"] = amount
    return _signed_post("/v5/account/no-convert-repay", params)


@mcp.tool()
def manual_repay(coin: str = "", amount: str = "") -> Any:
    """
    Manual repay (with auto conversion if needed).

    Args:
        coin: Coin to repay (optional).
        amount: Repay amount (optional).
    """
    params: dict[str, str] = {}
    if coin:
        params["coin"] = coin
    if amount:
        params["amount"] = amount
    return _signed_post("/v5/account/repay", params)


@mcp.tool()
def repay_liability(coin: str = "") -> Any:
    """
    Quick repay liability.

    Args:
        coin: Coin with liability (optional, repays all if empty).
    """
    params: dict[str, str] = {}
    if coin:
        params["coin"] = coin
    return _signed_post("/v5/account/quick-repayment", params)


@mcp.tool()
def reset_mmp(base_coin: str) -> Any:
    """
    Reset Market Maker Protection (MMP).

    Args:
        base_coin: Base coin, e.g., BTC.
    """
    return _signed_post("/v5/account/mmp-reset", {"baseCoin": base_coin})


@mcp.tool()
def set_collateral_coin(coin: str, collateral_switch: str) -> Any:
    """
    Set collateral coin on or off.

    Args:
        coin: Coin name (USDT/USDC cannot be set).
        collateral_switch: "ON" or "OFF".
    """
    return _signed_post("/v5/account/set-collateral-switch", {
        "coin": coin, "collateralSwitch": collateral_switch,
    })


@mcp.tool()
def set_margin_mode(margin_mode: str) -> Any:
    """
    Set account margin mode.

    Args:
        margin_mode: ISOLATED_MARGIN, REGULAR_MARGIN, or PORTFOLIO_MARGIN.
    """
    return _signed_post("/v5/account/set-margin-mode", {"setMarginMode": margin_mode})


@mcp.tool()
def set_mmp(base_coin: str, window: str, frozen_period: str, qty_limit: str, delta_limit: str) -> Any:
    """
    Set Market Maker Protection (MMP) parameters.

    Args:
        base_coin: Base coin, e.g., BTC.
        window: Time window in ms.
        frozen_period: Frozen period in ms.
        qty_limit: Trade quantity limit.
        delta_limit: Delta limit.
    """
    return _signed_post("/v5/account/mmp-modify", {
        "baseCoin": base_coin, "window": window, "frozenPeriod": frozen_period,
        "qtyLimit": qty_limit, "deltaLimit": delta_limit,
    })


@mcp.tool()
def set_price_limit_behaviour(category: str, modify_enable: bool) -> Any:
    """
    Set price limit behaviour (allow system to modify order price or reject).

    Args:
        category: Product type: linear, inverse, spot.
        modify_enable: true: allow modify, false: reject.
    """
    return _signed_post("/v5/account/set-limit-px-action", {
        "category": category, "modifyEnable": modify_enable,
    })


@mcp.tool()
def set_spot_hedging(mode: str) -> Any:
    """
    Set spot hedging mode on or off.

    Args:
        mode: "ON" or "OFF".
    """
    return _signed_post("/v5/account/set-hedging-mode", {"setHedgingMode": mode})


@mcp.tool()
def get_smp_group() -> Any:
    """Get Self Match Prevention (SMP) group ID."""
    return _signed_get("/v5/account/smp-group", {})


@mcp.tool()
def get_transferable_amount(coin_name: str) -> Any:
    """
    Get transferable amount for unified account.

    Args:
        coin_name: Coin name(s), comma-separated for multiple (max 20), e.g., "BTC,ETH".
    """
    return _signed_get("/v5/account/withdrawal", {"coinName": coin_name})


@mcp.tool()
def upgrade_to_uta() -> Any:
    """Upgrade account to Unified Trading Account (UTA)."""
    return _signed_post("/v5/account/upgrade-to-uta", {})
