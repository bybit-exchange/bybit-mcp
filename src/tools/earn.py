from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def earn_place_order(
    category: str,
    order_type: str,
    account_type: str,
    amount: str,
    coin: str,
    product_id: str,
    order_link_id: str,
) -> Any:
    """
    Stake or redeem in Bybit Earn.

    Args:
        category: Product category, e.g., FlexibleSaving, StakingProduct.
        order_type: Order type: Stake, Redeem.
        account_type: Account type: UNIFIED, FUND.
        amount: Amount to stake or redeem.
        coin: Coin name, e.g., USDT.
        product_id: Product ID.
        order_link_id: Unique order link ID.
    """
    return _signed_post("/v5/earn/place-order", {
        "category": category, "orderType": order_type, "accountType": account_type,
        "amount": amount, "coin": coin, "productId": product_id, "orderLinkId": order_link_id,
    })


@mcp.tool()
def get_earn_hourly_yield(category: str, product_id: str = "", limit: int = 50) -> Any:
    """
    Get Earn hourly yield history.

    Args:
        category: Product category.
        product_id: Filter by product ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if product_id:
        params["productId"] = product_id
    return _signed_get("/v5/earn/hourly-yield", params)


@mcp.tool()
def get_earn_order_history(category: str, product_id: str = "", limit: int = 50) -> Any:
    """
    Get Earn stake/redeem order history.

    Args:
        category: Product category.
        product_id: Filter by product ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if product_id:
        params["productId"] = product_id
    return _signed_get("/v5/earn/order", params)


@mcp.tool()
def get_earn_position(category: str, product_id: str = "", coin: str = "") -> Any:
    """
    Get Earn staked position.

    Args:
        category: Product category.
        product_id: Filter by product ID (optional).
        coin: Filter by coin (optional).
    """
    params: dict[str, str] = {"category": category}
    if product_id:
        params["productId"] = product_id
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/earn/position", params)


@mcp.tool()
def get_earn_product(category: str, coin: str = "") -> Any:
    """
    Get Earn product info.

    Args:
        category: Product category.
        coin: Filter by coin (optional).
    """
    params: dict[str, str] = {"category": category}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/earn/product", params)


@mcp.tool()
def get_earn_yield_history(category: str, product_id: str = "", limit: int = 50) -> Any:
    """
    Get Earn yield history.

    Args:
        category: Product category.
        product_id: Filter by product ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if product_id:
        params["productId"] = product_id
    return _signed_get("/v5/earn/yield", params)
