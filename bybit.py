import time
import hmac
import hashlib
import requests
import json
from functools import lru_cache
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bybit MCP Server")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--bybit-api-key", type=str, default="",
                    help="Bybit API Key")
parser.add_argument("--bybit-secret-key", type=str, default="",
                    help="Bybit Secret Key")
parser.add_argument("--testnet", action="store_true",
                    help="Use Bybit testnet")
args = parser.parse_args()

BYBIT_API_KEY = args.bybit_api_key
BYBIT_SECRET_KEY = args.bybit_secret_key
BASE_URL = "https://api-testnet.bybit.com" if args.testnet else "https://api.bybit.com"
RECV_WINDOW = "5000"


def _sign_request(timestamp: str, params: str) -> str:
    """Generate HMAC-SHA256 signature for Bybit V5 API."""
    param_str = f"{timestamp}{BYBIT_API_KEY}{RECV_WINDOW}{params}"
    return hmac.new(
        BYBIT_SECRET_KEY.encode("utf-8"),
        param_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def _auth_headers(timestamp: str, signature: str) -> dict:
    """Build authenticated request headers."""
    return {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-SIGN": signature,
        "X-BAPI-SIGN-TYPE": "2",
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": RECV_WINDOW,
        "Content-Type": "application/json",
    }


def _signed_get(endpoint: str, params: dict) -> dict:
    """Make a signed GET request to Bybit V5 API."""
    timestamp = str(int(time.time() * 1000))
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = _sign_request(timestamp, query_string)
    headers = _auth_headers(timestamp, signature)
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    data = response.json()
    if data.get("retCode") == 0:
        return data.get("result", {})
    return {"error": data.get("retMsg", "Unknown error"), "retCode": data.get("retCode")}


def _signed_post(endpoint: str, params: dict) -> dict:
    """Make a signed POST request to Bybit V5 API."""
    timestamp = str(int(time.time() * 1000))
    body = json.dumps(params)
    signature = _sign_request(timestamp, body)
    headers = _auth_headers(timestamp, signature)
    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, data=body)
    data = response.json()
    if data.get("retCode") == 0:
        return data.get("result", {})
    return {"error": data.get("retMsg", "Unknown error"), "retCode": data.get("retCode")}


@mcp.tool()
@lru_cache(maxsize=100)
def get_symbol_price(symbol: str, category: str = "spot") -> Any:
    """
    Get the current price of a cryptocurrency pair.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse (default: spot).

    Returns:
        Price information from Bybit.
    """
    url = f"{BASE_URL}/v5/market/tickers"
    params = {"category": category, "symbol": symbol}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("retCode") == 0:
        tickers = data["result"].get("list", [])
        if tickers:
            return {"symbol": symbol, "price": tickers[0]["lastPrice"]}
    return {"error": data.get("retMsg", "Unknown error")}


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
def get_funding_rate_history(symbol: str, category: str = "linear", limit: int = 100) -> Any:
    """
    Get funding rate history for a perpetual contract.

    Args:
        symbol: Perpetual contract symbol, e.g., BTCUSDT.
        category: Product type: linear, inverse (default: linear).
        limit: Number of records to return (default: 100, max: 200).

    Returns:
        Funding rate data list.
    """
    url = f"{BASE_URL}/v5/market/funding/history"
    params = {"category": category, "symbol": symbol, "limit": str(limit)}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("retCode") == 0:
        return data["result"].get("list", [])
    return {"error": data.get("retMsg", "Unknown error")}


@mcp.tool()
def get_kline(symbol: str, interval: str = "60", category: str = "spot", limit: int = 100) -> Any:
    """
    Get kline/candlestick data.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        interval: Kline interval: 1,3,5,15,30,60,120,240,360,720,D,M,W (default: 60).
        category: Product type: spot, linear, inverse (default: spot).
        limit: Number of records (default: 100, max: 1000).

    Returns:
        List of kline data [startTime, openPrice, highPrice, lowPrice, closePrice, volume, turnover].
    """
    url = f"{BASE_URL}/v5/market/kline"
    params = {"category": category, "symbol": symbol, "interval": interval, "limit": str(limit)}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("retCode") == 0:
        return data["result"].get("list", [])
    return {"error": data.get("retMsg", "Unknown error")}


@mcp.tool()
def get_orderbook(symbol: str, category: str = "spot", limit: int = 25) -> Any:
    """
    Get order book depth data.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse (default: spot).
        limit: Depth limit: 1-200 (default: 25).

    Returns:
        Order book with bids and asks.
    """
    url = f"{BASE_URL}/v5/market/orderbook"
    params = {"category": category, "symbol": symbol, "limit": str(limit)}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("retCode") == 0:
        return data["result"]
    return {"error": data.get("retMsg", "Unknown error")}


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
def get_instruments_info(symbol: str, category: str = "spot") -> Any:
    """
    Get instrument specification info.

    Args:
        symbol: The trading pair, e.g., BTCUSDT.
        category: Product type: spot, linear, inverse, option (default: spot).

    Returns:
        Instrument specification details including lot size, price filter, etc.
    """
    url = f"{BASE_URL}/v5/market/instruments-info"
    params = {"category": category, "symbol": symbol}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("retCode") == 0:
        instruments = data["result"].get("list", [])
        if instruments:
            return instruments[0]
    return {"error": data.get("retMsg", "Unknown error")}


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
        "message": f"Arbitrage executed. Estimated net profit: {net_profit:.4f} USDT"
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
    tickers_url = f"{BASE_URL}/v5/market/tickers"
    funding_url = f"{BASE_URL}/v5/market/funding/history"
    candidates = []

    response = requests.get(tickers_url, params={"category": "linear"})
    data = response.json()
    if data.get("retCode") != 0:
        return [{"error": "Failed to fetch tickers"}]

    for ticker in data["result"].get("list", []):
        try:
            symbol = ticker["symbol"]
            current_rate = float(ticker.get("fundingRate", 0))
            volume = float(ticker.get("turnover24h", 0))

            if abs(current_rate) < min_funding_rate or volume < min_avg_volume:
                continue

            history_resp = requests.get(funding_url, params={
                "category": "linear",
                "symbol": symbol,
                "limit": str(history_limit),
            })
            history_data = history_resp.json()
            if history_data.get("retCode") != 0:
                continue

            rates = [float(x["fundingRate"]) for x in history_data["result"].get("list", [])]
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


if __name__ == "__main__":
    mcp.run(transport="stdio")
