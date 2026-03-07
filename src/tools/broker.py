from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def get_broker_earning_record(biz_type: str = "", limit: int = 50) -> Any:
    """
    Get broker earning record (deprecated, use get_broker_earnings_info).

    Args:
        biz_type: Business type filter (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if biz_type:
        params["bizType"] = biz_type
    return _signed_get("/v5/broker/earning-record", params)


@mcp.tool()
def get_broker_account_info() -> Any:
    """Get broker account info."""
    return _signed_get("/v5/broker/account-info", {})


@mcp.tool()
def get_broker_earnings_info(biz_type: str = "", limit: int = 50) -> Any:
    """
    Get broker earnings info.

    Args:
        biz_type: Business type filter (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if biz_type:
        params["bizType"] = biz_type
    return _signed_get("/v5/broker/earnings-info", params)


@mcp.tool()
def get_broker_all_rate_limits(limit: int = 50) -> Any:
    """
    Get all broker rate limits.

    Args:
        limit: Number of records (default: 50).
    """
    return _signed_get("/v5/broker/apilimit/query-all", {"limit": str(limit)})


@mcp.tool()
def get_broker_rate_limit_cap() -> Any:
    """Get broker rate limit cap."""
    return _signed_get("/v5/broker/apilimit/query-cap", {})


@mcp.tool()
def set_broker_rate_limit(rate_limits: list[dict]) -> Any:
    """
    Set broker rate limits.

    Args:
        rate_limits: List of rate limit objects, each with: uids, bizType, rate.
    """
    return _signed_post("/v5/broker/apilimit/set", {"list": rate_limits})


@mcp.tool()
def get_broker_sub_deposit_record(sub_member_id: str = "", coin: str = "", limit: int = 50) -> Any:
    """
    Get broker sub account deposit records.

    Args:
        sub_member_id: Sub member ID (optional).
        coin: Filter by coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if sub_member_id:
        params["subMemberId"] = sub_member_id
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/broker/asset/query-sub-member-deposit-record", params)


@mcp.tool()
def get_broker_voucher_spec(voucher_id: str) -> Any:
    """
    Get broker voucher specification.

    Args:
        voucher_id: Voucher/award ID.
    """
    return _signed_post("/v5/broker/award/info", {"id": voucher_id})


@mcp.tool()
def issue_broker_voucher(account_id: str, award_id: str, spec_code: str, amount: str, broker_id: str) -> Any:
    """
    Issue a broker voucher/award.

    Args:
        account_id: Target account ID.
        award_id: Award ID.
        spec_code: Spec code.
        amount: Amount.
        broker_id: Broker ID.
    """
    return _signed_post("/v5/broker/award/distribute-award", {
        "accountId": account_id, "awardId": award_id,
        "specCode": spec_code, "amount": amount, "brokerId": broker_id,
    })


@mcp.tool()
def get_broker_issued_voucher(account_id: str, award_id: str, spec_code: str) -> Any:
    """
    Get broker issued voucher record.

    Args:
        account_id: Target account ID.
        award_id: Award ID.
        spec_code: Spec code.
    """
    return _signed_post("/v5/broker/award/distribution-record", {
        "accountId": account_id, "awardId": award_id, "specCode": spec_code,
    })
