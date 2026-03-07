from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post, _public_get


@mcp.tool()
def get_rfq_config() -> Any:
    """Get RFQ configuration (counterparties, supported coins, etc.)."""
    return _signed_get("/v5/rfq/config", {})


@mcp.tool()
def create_rfq(counterparties: list[str], legs: list[dict], rfq_link_id: str = "") -> Any:
    """
    Create an RFQ (Request for Quote).

    Args:
        counterparties: List of counterparty UIDs.
        legs: List of leg dicts, each with: category, symbol, side, qty.
        rfq_link_id: Unique RFQ link ID (optional).
    """
    params: dict[str, Any] = {"counterparties": counterparties, "list": legs}
    if rfq_link_id:
        params["rfqLinkId"] = rfq_link_id
    return _signed_post("/v5/rfq/create-rfq", params)


@mcp.tool()
def cancel_rfq(rfq_id: str = "", rfq_link_id: str = "") -> Any:
    """
    Cancel an RFQ.

    Args:
        rfq_id: RFQ ID (either rfq_id or rfq_link_id required).
        rfq_link_id: RFQ link ID.
    """
    params: dict[str, str] = {}
    if rfq_id:
        params["rfqId"] = rfq_id
    if rfq_link_id:
        params["rfqLinkId"] = rfq_link_id
    return _signed_post("/v5/rfq/cancel-rfq", params)


@mcp.tool()
def cancel_all_rfqs() -> Any:
    """Cancel all open RFQs."""
    return _signed_post("/v5/rfq/cancel-all-rfq", {})


@mcp.tool()
def accept_rfq_non_lp_quote(rfq_id: str) -> Any:
    """
    Accept a non-LP quote for an RFQ.

    Args:
        rfq_id: RFQ ID.
    """
    return _signed_post("/v5/rfq/accept-other-quote", {"rfqId": rfq_id})


@mcp.tool()
def create_rfq_quote(rfq_id: str, quote_link_id: str = "") -> Any:
    """
    Create a quote for an RFQ.

    Args:
        rfq_id: RFQ ID to quote against.
        quote_link_id: Unique quote link ID (optional).
    """
    params: dict[str, str] = {"rfqId": rfq_id}
    if quote_link_id:
        params["quoteLinkId"] = quote_link_id
    return _signed_post("/v5/rfq/create-quote", params)


@mcp.tool()
def cancel_rfq_quote(quote_id: str = "", rfq_id: str = "", quote_link_id: str = "") -> Any:
    """
    Cancel a quote.

    Args:
        quote_id: Quote ID (one of quote_id, rfq_id, or quote_link_id required).
        rfq_id: RFQ ID.
        quote_link_id: Quote link ID.
    """
    params: dict[str, str] = {}
    if quote_id:
        params["quoteId"] = quote_id
    if rfq_id:
        params["rfqId"] = rfq_id
    if quote_link_id:
        params["quoteLinkId"] = quote_link_id
    return _signed_post("/v5/rfq/cancel-quote", params)


@mcp.tool()
def cancel_all_rfq_quotes() -> Any:
    """Cancel all open quotes."""
    return _signed_post("/v5/rfq/cancel-all-quotes", {})


@mcp.tool()
def execute_rfq_quote(rfq_id: str, quote_id: str, quote_side: str) -> Any:
    """
    Execute (fill) a quote.

    Args:
        rfq_id: RFQ ID.
        quote_id: Quote ID.
        quote_side: Quote side: maker, taker.
    """
    return _signed_post("/v5/rfq/execute-quote", {
        "rfqId": rfq_id, "quoteId": quote_id, "quoteSide": quote_side,
    })


@mcp.tool()
def get_rfq_public_trades(limit: int = 50) -> Any:
    """
    Get RFQ public trades.

    Args:
        limit: Number of records (default: 50).
    """
    return _public_get("/v5/rfq/public-trades", {"limit": str(limit)})


@mcp.tool()
def get_rfq_quote_list(rfq_id: str = "", limit: int = 50) -> Any:
    """
    Get RFQ quotes list.

    Args:
        rfq_id: Filter by RFQ ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if rfq_id:
        params["rfqId"] = rfq_id
    return _signed_get("/v5/rfq/quote-list", params)


@mcp.tool()
def get_rfq_quote_realtime(rfq_id: str = "") -> Any:
    """
    Get RFQ quotes in real-time.

    Args:
        rfq_id: Filter by RFQ ID (optional).
    """
    params: dict[str, str] = {}
    if rfq_id:
        params["rfqId"] = rfq_id
    return _signed_get("/v5/rfq/quote-realtime", params)


@mcp.tool()
def get_rfq_list(rfq_id: str = "", limit: int = 50) -> Any:
    """
    Get RFQ list.

    Args:
        rfq_id: Filter by RFQ ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if rfq_id:
        params["rfqId"] = rfq_id
    return _signed_get("/v5/rfq/rfq-list", params)


@mcp.tool()
def get_rfq_realtime(rfq_id: str = "") -> Any:
    """
    Get RFQs in real-time.

    Args:
        rfq_id: Filter by RFQ ID (optional).
    """
    params: dict[str, str] = {}
    if rfq_id:
        params["rfqId"] = rfq_id
    return _signed_get("/v5/rfq/rfq-realtime", params)


@mcp.tool()
def get_rfq_trade_list(rfq_id: str = "", limit: int = 50) -> Any:
    """
    Get RFQ trade history.

    Args:
        rfq_id: Filter by RFQ ID (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if rfq_id:
        params["rfqId"] = rfq_id
    return _signed_get("/v5/rfq/trade-list", params)
