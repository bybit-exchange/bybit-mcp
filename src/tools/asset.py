from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


@mcp.tool()
def get_coin_balance(coin: str, account_type: str = "UNIFIED") -> Any:
    """
    Get the balance of a specific coin in a specific account type.

    Args:
        coin: The cryptocurrency symbol, e.g., BTC.
        account_type: Account type: UNIFIED, CONTRACT, SPOT, FUND (default: UNIFIED).

    Returns:
        Coin balance details.
    """
    result = _signed_get("/v5/asset/transfer/query-account-coin-balance", {
        "coin": coin, "accountType": account_type,
    })
    if "error" in result:
        return result
    return result.get("balance", result)


@mcp.tool()
def get_deposit_records(coin: str = "", limit: int = 50) -> Any:
    """
    Get deposit records.

    Args:
        coin: Filter by coin (optional).
        limit: Number of records (default: 50, max: 50).

    Returns:
        List of deposit records.
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    result = _signed_get("/v5/asset/deposit/query-record", params)
    if "error" in result:
        return result
    return result.get("rows", [])


@mcp.tool()
def get_withdrawal_records(coin: str = "", limit: int = 50) -> Any:
    """
    Get withdrawal records.

    Args:
        coin: Filter by coin (optional).
        limit: Number of records (default: 50, max: 50).

    Returns:
        List of withdrawal records.
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    result = _signed_get("/v5/asset/withdraw/query-record", params)
    if "error" in result:
        return result
    return result.get("rows", [])


@mcp.tool()
def create_internal_transfer(
    coin: str,
    amount: str,
    from_account_type: str,
    to_account_type: str,
    transfer_id: str = "",
) -> Any:
    """
    Create an internal transfer between account types.

    Args:
        coin: Coin to transfer, e.g., USDT.
        amount: Amount to transfer.
        from_account_type: Source account: UNIFIED, CONTRACT, SPOT, FUND.
        to_account_type: Destination account: UNIFIED, CONTRACT, SPOT, FUND.
        transfer_id: Unique transfer ID (UUID). Auto-generated if not provided.

    Returns:
        Transfer result.
    """
    import uuid
    params = {
        "transferId": transfer_id or str(uuid.uuid4()),
        "coin": coin,
        "amount": amount,
        "fromAccountType": from_account_type,
        "toAccountType": to_account_type,
    }
    result = _signed_post("/v5/asset/transfer/inter-transfer", params)
    if "error" in result:
        return result
    return {
        "message": f"Transferred {amount} {coin} from {from_account_type} to {to_account_type}",
        "transferId": result.get("transferId", ""),
    }


@mcp.tool()
def get_all_coins_balance(account_type: str, coin: str = "") -> Any:
    """
    Get all coins balance for an account type.

    Args:
        account_type: UNIFIED, CONTRACT, SPOT, FUND.
        coin: Filter by coin (optional).
    """
    params: dict[str, str] = {"accountType": account_type}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/transfer/query-account-coins-balance", params)


@mcp.tool()
def get_withdrawable_amount(coin: str) -> Any:
    """
    Get withdrawable amount for a coin.

    Args:
        coin: Coin name, e.g., USDT.
    """
    return _signed_get("/v5/asset/withdraw/withdrawable-amount", {"coin": coin})


@mcp.tool()
def get_coin_info(coin: str = "") -> Any:
    """
    Get coin info (chains, deposit/withdraw status, fees).

    Args:
        coin: Filter by coin (optional, returns all if empty).
    """
    params: dict[str, str] = {}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/coin/query-info", params)


@mcp.tool()
def get_small_balance_coins(account_type: str) -> Any:
    """
    Get small balance coins eligible for conversion.

    Args:
        account_type: Account type: UNIFIED, FUND.
    """
    return _signed_get("/v5/asset/covert/small-balance-list", {"accountType": account_type})


@mcp.tool()
def request_small_balance_quote(account_type: str, from_coin_list: list[str], to_coin: str) -> Any:
    """
    Request a quote for converting small balance coins.

    Args:
        account_type: Account type: UNIFIED, FUND.
        from_coin_list: List of coins to convert from.
        to_coin: Coin to convert to (e.g., USDT).
    """
    return _signed_post("/v5/asset/covert/get-quote", {
        "accountType": account_type, "fromCoinList": from_coin_list, "toCoin": to_coin,
    })


@mcp.tool()
def confirm_small_balance_quote(quote_id: str) -> Any:
    """
    Confirm a small balance conversion quote.

    Args:
        quote_id: Quote ID from request_small_balance_quote.
    """
    return _signed_post("/v5/asset/covert/small-balance-execute", {"quoteId": quote_id})


@mcp.tool()
def get_small_balance_exchange_history(account_type: str = "", limit: int = 50) -> Any:
    """
    Get small balance exchange history.

    Args:
        account_type: Filter by account type (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"size": str(limit)}
    if account_type:
        params["accountType"] = account_type
    return _signed_get("/v5/asset/covert/small-balance-history", params)


@mcp.tool()
def get_convert_coin_list(account_type: str, coin: str = "", side: str = "") -> Any:
    """
    Get available coins for crypto-to-crypto conversion.

    Args:
        account_type: UNIFIED or eb_convert_funding.
        coin: Filter by coin (optional).
        side: 0: from coin, 1: to coin (optional).
    """
    params: dict[str, str] = {"accountType": account_type}
    if coin:
        params["coin"] = coin
    if side:
        params["side"] = side
    return _signed_get("/v5/asset/exchange/query-coin-list", params)


@mcp.tool()
def request_convert_quote(account_type: str, from_coin: str, to_coin: str, request_coin: str, request_amount: str) -> Any:
    """
    Request a quote for crypto-to-crypto conversion.

    Args:
        account_type: UNIFIED or eb_convert_funding.
        from_coin: Source coin.
        to_coin: Destination coin.
        request_coin: The coin to specify amount for (from_coin or to_coin).
        request_amount: Amount of the request_coin.
    """
    return _signed_post("/v5/asset/exchange/quote-apply", {
        "accountType": account_type, "fromCoin": from_coin, "toCoin": to_coin,
        "requestCoin": request_coin, "requestAmount": request_amount,
    })


@mcp.tool()
def confirm_convert_quote(quote_tx_id: str) -> Any:
    """
    Confirm a crypto-to-crypto conversion quote.

    Args:
        quote_tx_id: Quote transaction ID.
    """
    return _signed_post("/v5/asset/exchange/convert-execute", {"quoteTxId": quote_tx_id})


@mcp.tool()
def get_convert_status(quote_tx_id: str, account_type: str) -> Any:
    """
    Get crypto-to-crypto conversion status.

    Args:
        quote_tx_id: Quote transaction ID.
        account_type: Account type.
    """
    return _signed_get("/v5/asset/exchange/convert-result-query", {
        "quoteTxId": quote_tx_id, "accountType": account_type,
    })


@mcp.tool()
def get_convert_history(account_type: str = "", limit: int = 50) -> Any:
    """
    Get crypto-to-crypto conversion history.

    Args:
        account_type: Filter by account type (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if account_type:
        params["accountType"] = account_type
    return _signed_get("/v5/asset/exchange/query-convert-history", params)


@mcp.tool()
def get_delivery_record(category: str, symbol: str = "", limit: int = 20) -> Any:
    """
    Get delivery record.

    Args:
        category: Product type: option, linear, inverse.
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/asset/delivery-record", params)


@mcp.tool()
def get_settlement_record(category: str, symbol: str = "", limit: int = 20) -> Any:
    """
    Get USDC session settlement record.

    Args:
        category: Product type: linear.
        symbol: Filter by symbol (optional).
        limit: Number of records (default: 20, max: 50).
    """
    params: dict[str, str] = {"category": category, "limit": str(limit)}
    if symbol:
        params["symbol"] = symbol
    return _signed_get("/v5/asset/settlement-record", params)


@mcp.tool()
def get_internal_deposit_records(coin: str = "", limit: int = 50) -> Any:
    """
    Get internal (off-chain) deposit records.

    Args:
        coin: Filter by coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/deposit/query-internal-record", params)


@mcp.tool()
def get_master_deposit_address(coin: str, chain_type: str = "") -> Any:
    """
    Get master deposit address.

    Args:
        coin: Coin name, e.g., BTC.
        chain_type: Chain type (optional).
    """
    params: dict[str, str] = {"coin": coin}
    if chain_type:
        params["chainType"] = chain_type
    return _signed_get("/v5/asset/deposit/query-address", params)


@mcp.tool()
def set_deposit_account(account_type: str) -> Any:
    """
    Set deposit account type.

    Args:
        account_type: UNIFIED, SPOT, FUND, etc.
    """
    return _signed_post("/v5/asset/deposit/deposit-to-account", {"accountType": account_type})


@mcp.tool()
def get_sub_deposit_address(coin: str, chain_type: str, sub_member_id: str) -> Any:
    """
    Get sub account deposit address.

    Args:
        coin: Coin name, e.g., BTC.
        chain_type: Chain type, e.g., ETH.
        sub_member_id: Sub UID.
    """
    return _signed_get("/v5/asset/deposit/query-sub-member-address", {
        "coin": coin, "chainType": chain_type, "subMemberId": sub_member_id,
    })


@mcp.tool()
def get_sub_deposit_records(sub_member_id: str, coin: str = "", limit: int = 50) -> Any:
    """
    Get sub account on-chain deposit records.

    Args:
        sub_member_id: Sub UID.
        coin: Filter by coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"subMemberId": sub_member_id, "limit": str(limit)}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/deposit/query-sub-member-record", params)


@mcp.tool()
def get_allowed_deposit_coins(coin: str = "", limit: int = 50) -> Any:
    """
    Get allowed deposit coin info.

    Args:
        coin: Filter by coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/deposit/query-allowed-list", params)


@mcp.tool()
def get_coin_exchange_records(from_coin: str = "", to_coin: str = "", limit: int = 50) -> Any:
    """
    Get coin exchange records.

    Args:
        from_coin: Source coin (optional).
        to_coin: Destination coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if from_coin:
        params["fromCoin"] = from_coin
    if to_coin:
        params["toCoin"] = to_coin
    return _signed_get("/v5/asset/exchange/order-record", params)


@mcp.tool()
def get_asset_sub_uid_list() -> Any:
    """Get sub UID list for asset transfers."""
    return _signed_get("/v5/asset/transfer/query-sub-member-list", {})


@mcp.tool()
def get_internal_transfer_records(coin: str = "", limit: int = 50) -> Any:
    """
    Get internal transfer records.

    Args:
        coin: Filter by coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/transfer/query-inter-transfer-list", params)


@mcp.tool()
def get_transferable_coin(from_account_type: str, to_account_type: str) -> Any:
    """
    Get transferable coins between account types.

    Args:
        from_account_type: Source account type.
        to_account_type: Destination account type.
    """
    return _signed_get("/v5/asset/transfer/query-transfer-coin-list", {
        "fromAccountType": from_account_type, "toAccountType": to_account_type,
    })


@mcp.tool()
def create_universal_transfer(
    coin: str,
    amount: str,
    from_member_id: str,
    to_member_id: str,
    from_account_type: str,
    to_account_type: str,
    transfer_id: str = "",
) -> Any:
    """
    Create a universal transfer (between sub UIDs or master-sub).

    Args:
        coin: Coin to transfer.
        amount: Amount to transfer.
        from_member_id: Source UID.
        to_member_id: Destination UID.
        from_account_type: Source account type.
        to_account_type: Destination account type.
        transfer_id: Unique transfer ID (UUID). Auto-generated if not provided.
    """
    import uuid
    return _signed_post("/v5/asset/transfer/universal-transfer", {
        "transferId": transfer_id or str(uuid.uuid4()),
        "coin": coin, "amount": amount,
        "fromMemberId": from_member_id, "toMemberId": to_member_id,
        "fromAccountType": from_account_type, "toAccountType": to_account_type,
    })


@mcp.tool()
def get_universal_transfer_records(coin: str = "", limit: int = 50) -> Any:
    """
    Get universal transfer records.

    Args:
        coin: Filter by coin (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    return _signed_get("/v5/asset/transfer/query-universal-transfer-list", params)


@mcp.tool()
def withdraw(coin: str, address: str, amount: str, account_type: str = "FUND", chain: str = "") -> Any:
    """
    Withdraw funds to an external address.

    Args:
        coin: Coin to withdraw, e.g., USDT.
        address: Withdrawal address.
        amount: Amount to withdraw.
        account_type: Account type: FUND (default).
        chain: Chain type (optional, e.g., ETH, TRX).
    """
    import time as _time
    params: dict[str, str] = {
        "coin": coin, "address": address, "amount": amount,
        "accountType": account_type, "timestamp": str(int(_time.time() * 1000)),
    }
    if chain:
        params["chain"] = chain
    return _signed_post("/v5/asset/withdraw/create", params)


@mcp.tool()
def cancel_withdrawal(withdraw_id: str) -> Any:
    """
    Cancel a pending withdrawal.

    Args:
        withdraw_id: Withdrawal ID.
    """
    return _signed_post("/v5/asset/withdraw/cancel", {"id": withdraw_id})


@mcp.tool()
def get_vasp_list() -> Any:
    """Get available VASPs (Virtual Asset Service Providers) for travel rule compliance."""
    return _signed_get("/v5/asset/withdraw/vasp/list", {})


@mcp.tool()
def get_withdrawal_address_list(coin: str = "", chain: str = "", limit: int = 50) -> Any:
    """
    Get saved withdrawal address list.

    Args:
        coin: Filter by coin (optional).
        chain: Filter by chain (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if coin:
        params["coin"] = coin
    if chain:
        params["chain"] = chain
    return _signed_get("/v5/asset/withdraw/query-address", params)


@mcp.tool()
def get_fiat_balance(currency: str = "") -> Any:
    """
    Get fiat balance.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/fiat/balance-query", params)


@mcp.tool()
def get_fiat_coin_list(side: str = "") -> Any:
    """
    Get fiat trading pair list.

    Args:
        side: Filter by side (optional).
    """
    params: dict[str, str] = {}
    if side:
        params["side"] = side
    return _signed_get("/v5/fiat/query-coin-list", params)


@mcp.tool()
def request_fiat_quote(from_coin: str, from_coin_type: str, to_coin: str, to_coin_type: str, request_amount: str) -> Any:
    """
    Request a fiat conversion quote.

    Args:
        from_coin: Source coin/currency.
        from_coin_type: Source type: crypto, fiat.
        to_coin: Destination coin/currency.
        to_coin_type: Destination type: crypto, fiat.
        request_amount: Amount.
    """
    return _signed_post("/v5/fiat/quote-apply", {
        "fromCoin": from_coin, "fromCoinType": from_coin_type,
        "toCoin": to_coin, "toCoinType": to_coin_type,
        "requestAmount": request_amount,
    })


@mcp.tool()
def confirm_fiat_quote(quote_tx_id: str, sub_user_id: str) -> Any:
    """
    Confirm a fiat conversion quote.

    Args:
        quote_tx_id: Quote transaction ID.
        sub_user_id: Sub user ID.
    """
    return _signed_post("/v5/fiat/trade-execute", {
        "quoteTxId": quote_tx_id, "subUserId": sub_user_id,
    })


@mcp.tool()
def get_fiat_convert_status(trade_no: str = "", merchant_request_id: str = "") -> Any:
    """
    Get fiat conversion status.

    Args:
        trade_no: Trade number (optional).
        merchant_request_id: Merchant request ID (optional).
    """
    params: dict[str, str] = {}
    if trade_no:
        params["tradeNo"] = trade_no
    if merchant_request_id:
        params["merchantRequestId"] = merchant_request_id
    return _signed_get("/v5/fiat/trade-query", params)


@mcp.tool()
def get_fiat_convert_history(limit: int = 50) -> Any:
    """
    Get fiat conversion history.

    Args:
        limit: Number of records (default: 50).
    """
    return _signed_get("/v5/fiat/query-trade-history", {"limit": str(limit)})


@mcp.tool()
def get_fiat_reference_price(symbol: str) -> Any:
    """
    Get fiat reference price for a trading pair.

    Args:
        symbol: Trading pair symbol.
    """
    return _signed_get("/v5/fiat/reference-price", {"symbol": symbol})
