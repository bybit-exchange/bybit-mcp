import time
from typing import Any

import requests

from src import mcp
from src.client import config, _public_get
from src.tools.market import get_symbol_price, get_funding_rate_history
from src.tools.trade import place_market_order
from src.tools.account import get_account_balance


@mcp.tool()
def execute_hedge_arbitrage_strategy(symbol: str, quantity: str) -> Any:
    """
    Execute hedge arbitrage based on funding rate.
    Opens opposing positions in spot and linear perpetual to capture funding rate.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        quantity: Amount to trade.

    Returns:
        Summary of the arbitrage result.
    """
    coin = symbol.replace("USDT", "")
    balance_result = get_account_balance(coin)
    try:
        available_balance = float(balance_result.get("available_balance", 0))
    except (ValueError, TypeError):
        available_balance = 0

    actual_quantity = min(float(quantity), available_balance) if available_balance > 0 else 0
    if actual_quantity <= 0:
        return {"error": f"Insufficient {coin} balance."}

    funding_data = get_funding_rate_history(symbol, limit=1)
    if isinstance(funding_data, dict) and "error" in funding_data:
        return funding_data
    if not funding_data:
        return {"error": "No funding rate data available"}

    funding_rate = float(funding_data[0].get("fundingRate", 0))
    price_data = get_symbol_price(symbol)
    if "error" in price_data:
        return price_data
    spot_price = float(price_data["price"])

    qty_str = str(actual_quantity)

    if funding_rate > 0:
        place_market_order(symbol, "Buy", qty_str, "spot")
        place_market_order(symbol, "Sell", qty_str, "linear")
    else:
        place_market_order(symbol, "Sell", qty_str, "spot")
        place_market_order(symbol, "Buy", qty_str, "linear")

    time.sleep(10)

    if funding_rate > 0:
        place_market_order(symbol, "Buy", qty_str, "linear")
        place_market_order(symbol, "Sell", qty_str, "spot")
    else:
        place_market_order(symbol, "Sell", qty_str, "linear")
        place_market_order(symbol, "Buy", qty_str, "spot")

    SPOT_FEE = 0.001
    FUTURES_FEE = 0.0002
    fee = (spot_price * actual_quantity * SPOT_FEE * 2) + (spot_price * actual_quantity * FUTURES_FEE * 2)
    profit = abs(funding_rate) * spot_price * actual_quantity
    net_profit = profit - fee

    return {
        "net_profit": round(net_profit, 4),
        "fees": round(fee, 4),
        "funding_rate": funding_rate,
        "message": f"Arbitrage executed. Estimated net profit: {net_profit:.4f} USDT",
    }


@mcp.tool()
def find_arbitrage_pairs(
    min_funding_rate: float = 0.0005,
    min_avg_volume: float = 1_000_000,
    history_limit: int = 21,
    stability_threshold: float = 0.8,
) -> list[dict[str, Any]]:
    """
    Find arbitrage pairs based on funding rate, volume, and rate direction stability.

    Args:
        min_funding_rate: Minimum absolute funding rate to qualify.
        min_avg_volume: Minimum 24hr volume in USDT.
        history_limit: Number of historical funding rate records to analyze.
        stability_threshold: Minimum proportion of funding rates in same direction.

    Returns:
        List of qualifying arbitrage opportunities.
    """
    candidates = []

    tickers_result = _public_get("/v5/market/tickers", {"category": "linear"})
    if "error" in tickers_result:
        return [{"error": "Failed to fetch tickers"}]

    for ticker in tickers_result.get("list", []):
        try:
            symbol = ticker["symbol"]
            current_rate = float(ticker.get("fundingRate", 0))
            volume = float(ticker.get("turnover24h", 0))

            if abs(current_rate) < min_funding_rate or volume < min_avg_volume:
                continue

            history_result = _public_get("/v5/market/funding/history", {
                "category": "linear",
                "symbol": symbol,
                "limit": str(history_limit),
            })
            if "error" in history_result:
                continue

            rates = [float(x["fundingRate"]) for x in history_result.get("list", [])]
            if not rates:
                continue

            same_dir = sum(1 for r in rates if (r > 0) == (current_rate > 0))
            stability = same_dir / len(rates)

            if stability >= stability_threshold:
                candidates.append({
                    "symbol": symbol,
                    "current_funding_rate": current_rate,
                    "avg_volume_24h": volume,
                    "stability": round(stability, 2),
                })
        except Exception:
            continue

    return sorted(candidates, key=lambda x: -abs(x["current_funding_rate"]))
