from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def get_api_key_info() -> Any:
    """Get current API key information (permissions, IP whitelist, etc.)."""
    return _signed_get("/v5/user/query-api", {})


@mcp.tool()
def create_sub_uid(username: str, member_type: int, note: str = "") -> Any:
    """
    Create a sub UID.

    Args:
        username: Sub account username (6-16 chars, letters+numbers).
        member_type: 1: normal sub account, 6: custodial sub account.
        note: Note for the sub account (optional).
    """
    params: dict[str, Any] = {"username": username, "memberType": member_type}
    if note:
        params["note"] = note
    return _signed_post("/v5/user/create-sub-member", params)


@mcp.tool()
def create_sub_api_key(sub_uid: int, read_only: int, permissions: dict) -> Any:
    """
    Create API key for a sub UID.

    Args:
        sub_uid: Sub UID.
        read_only: 0: Read and Write, 1: Read only.
        permissions: Permission object, e.g., {"ContractTrade": ["Order","Position"], "Spot": ["SpotTrade"]}.
    """
    return _signed_post("/v5/user/create-sub-api", {
        "subuid": sub_uid, "readOnly": read_only, "permissions": permissions,
    })


@mcp.tool()
def freeze_sub_uid(sub_uid: int, frozen: int) -> Any:
    """
    Freeze or unfreeze a sub UID.

    Args:
        sub_uid: Sub UID.
        frozen: 0: unfreeze, 1: freeze.
    """
    return _signed_post("/v5/user/frozen-sub-member", {"subuid": sub_uid, "frozen": frozen})


@mcp.tool()
def get_fund_custodial_sub_list() -> Any:
    """Get fund custodial sub account list."""
    return _signed_get("/v5/user/escrow_sub_members", {})


@mcp.tool()
def get_sub_api_keys(sub_member_id: str) -> Any:
    """
    Get all API keys of a sub account.

    Args:
        sub_member_id: Sub UID.
    """
    return _signed_get("/v5/user/sub-apikeys", {"subMemberId": sub_member_id})


@mcp.tool()
def modify_master_api_key(permissions: dict = {}, read_only: int = -1) -> Any:
    """
    Modify master API key permissions.

    Args:
        permissions: Permission object (optional).
        read_only: 0: Read and Write, 1: Read only (optional, -1 to skip).
    """
    params: dict[str, Any] = {}
    if permissions:
        params["permissions"] = permissions
    if read_only >= 0:
        params["readOnly"] = read_only
    return _signed_post("/v5/user/update-api", params)


@mcp.tool()
def modify_sub_api_key(apikey: str = "", permissions: dict = {}, read_only: int = -1) -> Any:
    """
    Modify sub API key permissions.

    Args:
        apikey: Sub API key (optional).
        permissions: Permission object (optional).
        read_only: 0: Read and Write, 1: Read only (optional, -1 to skip).
    """
    params: dict[str, Any] = {}
    if apikey:
        params["apikey"] = apikey
    if permissions:
        params["permissions"] = permissions
    if read_only >= 0:
        params["readOnly"] = read_only
    return _signed_post("/v5/user/update-sub-api", params)


@mcp.tool()
def get_sub_uid_list_paginated() -> Any:
    """Get sub UID list (unlimited, paginated)."""
    return _signed_get("/v5/user/submembers", {})


@mcp.tool()
def delete_master_api_key() -> Any:
    """Delete the current master API key."""
    return _signed_post("/v5/user/delete-api", {})


@mcp.tool()
def delete_sub_api_key(apikey: str = "") -> Any:
    """
    Delete a sub API key.

    Args:
        apikey: The sub API key to delete (optional).
    """
    params: dict[str, str] = {}
    if apikey:
        params["apikey"] = apikey
    return _signed_post("/v5/user/delete-sub-api", params)


@mcp.tool()
def delete_sub_uid(sub_member_id: str) -> Any:
    """
    Delete a sub UID.

    Args:
        sub_member_id: Sub UID to delete.
    """
    return _signed_post("/v5/user/del-submember", {"subMemberId": sub_member_id})


@mcp.tool()
def get_sub_uid_list() -> Any:
    """Get sub UID list (limited)."""
    return _signed_get("/v5/user/query-sub-members", {})


@mcp.tool()
def get_uid_wallet_type(member_ids: str = "") -> Any:
    """
    Get UID wallet type (UTA or classic).

    Args:
        member_ids: Comma-separated member IDs (optional).
    """
    params: dict[str, str] = {}
    if member_ids:
        params["memberIds"] = member_ids
    return _signed_get("/v5/user/get-member-type", params)


@mcp.tool()
def get_affiliate_user_info(uid: str) -> Any:
    """
    Get affiliate user info.

    Args:
        uid: The user UID.
    """
    return _signed_get("/v5/user/aff-customer-info", {"uid": uid})


@mcp.tool()
def get_affiliate_user_list(limit: int = 50) -> Any:
    """
    Get affiliate user list.

    Args:
        limit: Number of records (default: 50).
    """
    return _signed_get("/v5/affiliate/aff-user-list", {"size": str(limit)})
