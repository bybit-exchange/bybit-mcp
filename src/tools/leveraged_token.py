from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post, _public_get


@mcp.tool()
def get_leveraged_token_info(lt_coin: str = "") -> Any:
    """
    Get leveraged token info.

    Args:
        lt_coin: Leveraged token abbreviation, e.g., BTC3L (optional, returns all if empty).
    """
    params: dict[str, str] = {}
    if lt_coin:
        params["ltCoin"] = lt_coin
    return _public_get("/v5/spot-lever-token/info", params)


@mcp.tool()
def get_leveraged_token_market(lt_coin: str) -> Any:
    """
    Get leveraged token market data (NAV, leverage, etc.).

    Args:
        lt_coin: Leveraged token abbreviation, e.g., BTC3L.
    """
    return _public_get("/v5/spot-lever-token/reference", {"ltCoin": lt_coin})


@mcp.tool()
def get_leveraged_token_order_record(lt_coin: str = "", order_id: str = "", limit: int = 50) -> Any:
    """
    Get leveraged token purchase/redemption records.

    Args:
        lt_coin: Filter by leveraged token (optional).
        order_id: Filter by order ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if lt_coin:
        params["ltCoin"] = lt_coin
    if order_id:
        params["orderId"] = order_id
    return _signed_get("/v5/spot-lever-token/order-record", params)


@mcp.tool()
def purchase_leveraged_token(lt_coin: str, lt_amount: str, serial_no: str = "") -> Any:
    """
    Purchase a leveraged token.

    Args:
        lt_coin: Leveraged token abbreviation, e.g., BTC3L.
        lt_amount: Purchase amount in USDT.
        serial_no: Unique serial number (optional).
    """
    params: dict[str, str] = {"ltCoin": lt_coin, "ltAmount": lt_amount}
    if serial_no:
        params["serialNo"] = serial_no
    return _signed_post("/v5/spot-lever-token/purchase", params)


@mcp.tool()
def redeem_leveraged_token(lt_coin: str, quantity: str, serial_no: str = "") -> Any:
    """
    Redeem a leveraged token.

    Args:
        lt_coin: Leveraged token abbreviation, e.g., BTC3L.
        quantity: Redemption quantity.
        serial_no: Unique serial number (optional).
    """
    params: dict[str, str] = {"ltCoin": lt_coin, "quantity": quantity}
    if serial_no:
        params["serialNo"] = serial_no
    return _signed_post("/v5/spot-lever-token/redeem", params)
