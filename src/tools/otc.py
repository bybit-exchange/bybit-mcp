from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def otc_loan_bind_uid(uid: str, operate: str) -> Any:
    """
    Bind or unbind UID for OTC lending.

    Args:
        uid: UID to bind/unbind.
        operate: Operation: bind, unbind.
    """
    return _signed_post("/v5/ins-loan/association-uid", {"uid": uid, "operate": operate})


@mcp.tool()
def get_otc_loan_orders(order_id: str = "", limit: int = 50) -> Any:
    """
    Get OTC loan orders.

    Args:
        order_id: Filter by order ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if order_id:
        params["orderId"] = order_id
    return _signed_get("/v5/ins-loan/loan-order", params)


@mcp.tool()
def get_otc_loan_ltv() -> Any:
    """Get OTC loan LTV conversion info."""
    return _signed_get("/v5/ins-loan/ltv-convert", {})


@mcp.tool()
def get_otc_loan_margin_coin_info(product_id: str = "") -> Any:
    """
    Get OTC loan margin coin conversion info.

    Args:
        product_id: Filter by product ID (optional).
    """
    params: dict[str, str] = {}
    if product_id:
        params["productId"] = product_id
    return _signed_get("/v5/ins-loan/ensure-tokens-convert", params)


@mcp.tool()
def get_otc_loan_product_info(product_id: str = "") -> Any:
    """
    Get OTC loan product info.

    Args:
        product_id: Filter by product ID (optional).
    """
    params: dict[str, str] = {}
    if product_id:
        params["productId"] = product_id
    return _signed_get("/v5/ins-loan/product-infos", params)


@mcp.tool()
def otc_loan_repay(token: str, quantity: str) -> Any:
    """
    Repay OTC loan.

    Args:
        token: Repay token/coin.
        quantity: Repay amount.
    """
    return _signed_post("/v5/ins-loan/repay-loan", {"token": token, "quantity": quantity})


@mcp.tool()
def get_otc_loan_repay_history(limit: int = 50) -> Any:
    """
    Get OTC loan repayment history.

    Args:
        limit: Number of records (default: 50).
    """
    return _signed_get("/v5/ins-loan/repaid-history", {"limit": str(limit)})
