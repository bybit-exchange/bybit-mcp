from typing import Any

from src import mcp
from src.client import _signed_get, _signed_post


# --- Old Crypto Loan ---

@mcp.tool()
def crypto_loan_borrow(loan_currency: str, collateral_currency: str, loan_amount: str = "", collateral_amount: str = "") -> Any:
    """
    Borrow via crypto loan.

    Args:
        loan_currency: Loan currency, e.g., USDT.
        collateral_currency: Collateral currency, e.g., BTC.
        loan_amount: Loan amount (either loan_amount or collateral_amount required).
        collateral_amount: Collateral amount.
    """
    params: dict[str, str] = {"loanCurrency": loan_currency, "collateralCurrency": collateral_currency}
    if loan_amount:
        params["loanAmount"] = loan_amount
    if collateral_amount:
        params["collateralAmount"] = collateral_amount
    return _signed_post("/v5/crypto-loan/borrow", params)


@mcp.tool()
def crypto_loan_repay(order_id: str, amount: str) -> Any:
    """
    Repay a crypto loan.

    Args:
        order_id: Loan order ID.
        amount: Repay amount.
    """
    return _signed_post("/v5/crypto-loan/repay", {"orderId": order_id, "amount": amount})


@mcp.tool()
def crypto_loan_adjust_ltv(order_id: str, amount: str, direction: str) -> Any:
    """
    Adjust collateral amount (LTV) for a crypto loan.

    Args:
        order_id: Loan order ID.
        amount: Adjustment amount.
        direction: Direction: add, reduce.
    """
    return _signed_post("/v5/crypto-loan/adjust-ltv", {
        "orderId": order_id, "amount": amount, "direction": direction,
    })


@mcp.tool()
def get_crypto_loan_ongoing_orders(loan_currency: str = "", collateral_currency: str = "", limit: int = 50) -> Any:
    """
    Get ongoing (unpaid) crypto loan orders.

    Args:
        loan_currency: Filter by loan currency (optional).
        collateral_currency: Filter by collateral currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    if collateral_currency:
        params["collateralCurrency"] = collateral_currency
    return _signed_get("/v5/crypto-loan/ongoing-orders", params)


@mcp.tool()
def get_crypto_loan_borrow_history(loan_currency: str = "", limit: int = 50) -> Any:
    """
    Get crypto loan completed loan history.

    Args:
        loan_currency: Filter by loan currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_get("/v5/crypto-loan/borrow-history", params)


@mcp.tool()
def get_crypto_loan_repayment_history(loan_currency: str = "", limit: int = 50) -> Any:
    """
    Get crypto loan repayment history.

    Args:
        loan_currency: Filter by loan currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_get("/v5/crypto-loan/repayment-history", params)


@mcp.tool()
def get_crypto_loan_adjustment_history(collateral_currency: str = "", limit: int = 50) -> Any:
    """
    Get crypto loan LTV adjustment history.

    Args:
        collateral_currency: Filter by collateral currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if collateral_currency:
        params["collateralCurrency"] = collateral_currency
    return _signed_get("/v5/crypto-loan/adjustment-history", params)


@mcp.tool()
def get_crypto_loan_max_collateral(order_id: str) -> Any:
    """
    Get max allowed collateral reduction amount for a crypto loan.

    Args:
        order_id: Loan order ID.
    """
    return _signed_get("/v5/crypto-loan/max-collateral-amount", {"orderId": order_id})


@mcp.tool()
def get_crypto_loan_loanable_data(currency: str = "") -> Any:
    """
    Get loanable coin data (interest rates, limits).

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/crypto-loan/loanable-data", params)


@mcp.tool()
def get_crypto_loan_collateral_data(currency: str = "") -> Any:
    """
    Get collateral coin data (LTV ratios, limits).

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/crypto-loan/collateral-data", params)


@mcp.tool()
def get_crypto_loan_borrowable_collateralisable(loan_currency: str, collateral_currency: str) -> Any:
    """
    Get borrowable and collateralisable amount for account.

    Args:
        loan_currency: Loan currency, e.g., USDT.
        collateral_currency: Collateral currency, e.g., BTC.
    """
    return _signed_get("/v5/crypto-loan/borrowable-collateralisable-number", {
        "loanCurrency": loan_currency, "collateralCurrency": collateral_currency,
    })


# --- New Crypto Loan (Common) ---

@mcp.tool()
def new_crypto_loan_adjust_ltv(currency: str, amount: str, direction: str) -> Any:
    """
    Adjust collateral amount for new crypto loan.

    Args:
        currency: Collateral currency.
        amount: Adjustment amount.
        direction: Direction: add, reduce.
    """
    return _signed_post("/v5/crypto-loan-common/adjust-ltv", {
        "currency": currency, "amount": amount, "direction": direction,
    })


@mcp.tool()
def get_new_crypto_loan_collateral_data(currency: str = "") -> Any:
    """
    Get new crypto loan collateral coin data.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/crypto-loan-common/collateral-data", params)


@mcp.tool()
def get_new_crypto_loan_position() -> Any:
    """Get new crypto loan position info."""
    return _signed_get("/v5/crypto-loan-common/position", {})


@mcp.tool()
def get_new_crypto_loan_loanable_data(currency: str = "") -> Any:
    """
    Get new crypto loan loanable coin data.

    Args:
        currency: Filter by currency (optional).
    """
    params: dict[str, str] = {}
    if currency:
        params["currency"] = currency
    return _signed_get("/v5/crypto-loan-common/loanable-data", params)


@mcp.tool()
def get_new_crypto_loan_adjustment_history(collateral_currency: str = "", limit: int = 50) -> Any:
    """
    Get new crypto loan collateral adjustment history.

    Args:
        collateral_currency: Filter by collateral currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if collateral_currency:
        params["collateralCurrency"] = collateral_currency
    return _signed_get("/v5/crypto-loan-common/adjustment-history", params)


@mcp.tool()
def get_new_crypto_loan_max_loan(currency: str) -> Any:
    """
    Obtain max loan amount for new crypto loan.

    Args:
        currency: Loan currency.
    """
    return _signed_post("/v5/crypto-loan-common/max-loan", {"currency": currency})


@mcp.tool()
def get_new_crypto_loan_max_collateral(currency: str) -> Any:
    """
    Get max allowed collateral reduction amount (new crypto loan).

    Args:
        currency: Collateral currency.
    """
    return _signed_get("/v5/crypto-loan-common/max-collateral-amount", {"currency": currency})


# --- New Crypto Loan (Fixed) ---

@mcp.tool()
def new_crypto_loan_fixed_borrow(order_currency: str, order_amount: str, annual_rate: str, term: str) -> Any:
    """
    Create a fixed-term crypto loan borrow order.

    Args:
        order_currency: Borrow currency.
        order_amount: Borrow amount.
        annual_rate: Annual interest rate.
        term: Loan term in days.
    """
    return _signed_post("/v5/crypto-loan-fixed/borrow", {
        "orderCurrency": order_currency, "orderAmount": order_amount,
        "annualRate": annual_rate, "term": term,
    })


@mcp.tool()
def get_new_crypto_loan_fixed_contract_info(order_currency: str = "", limit: int = 50) -> Any:
    """
    Get fixed crypto loan borrow contract info.

    Args:
        order_currency: Filter by currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if order_currency:
        params["orderCurrency"] = order_currency
    return _signed_get("/v5/crypto-loan-fixed/borrow-contract-info", params)


@mcp.tool()
def get_new_crypto_loan_fixed_borrow_market(order_currency: str, order_by: str) -> Any:
    """
    Get fixed crypto loan borrowing market quotes.

    Args:
        order_currency: Borrow currency.
        order_by: Order by field.
    """
    return _signed_get("/v5/crypto-loan-fixed/borrow-order-quote", {
        "orderCurrency": order_currency, "orderBy": order_by,
    })


@mcp.tool()
def get_new_crypto_loan_fixed_borrow_order(order_currency: str = "", limit: int = 50) -> Any:
    """
    Get fixed crypto loan borrow order info.

    Args:
        order_currency: Filter by currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if order_currency:
        params["orderCurrency"] = order_currency
    return _signed_get("/v5/crypto-loan-fixed/borrow-order-info", params)


@mcp.tool()
def cancel_new_crypto_loan_fixed_borrow(order_id: str) -> Any:
    """
    Cancel a fixed crypto loan borrow order.

    Args:
        order_id: Borrow order ID.
    """
    return _signed_post("/v5/crypto-loan-fixed/borrow-order-cancel", {"orderId": order_id})


@mcp.tool()
def cancel_new_crypto_loan_fixed_supply(order_id: str) -> Any:
    """
    Cancel a fixed crypto loan supply order.

    Args:
        order_id: Supply order ID.
    """
    return _signed_post("/v5/crypto-loan-fixed/supply-order-cancel", {"orderId": order_id})


@mcp.tool()
def new_crypto_loan_fixed_renew(loan_id: str) -> Any:
    """
    Renew a fixed crypto loan borrow order.

    Args:
        loan_id: Loan ID.
    """
    return _signed_post("/v5/crypto-loan-fixed/renew", {"loanId": loan_id})


@mcp.tool()
def get_new_crypto_loan_fixed_renew_info(order_currency: str = "", limit: int = 50) -> Any:
    """
    Get fixed crypto loan renew order info.

    Args:
        order_currency: Filter by currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if order_currency:
        params["orderCurrency"] = order_currency
    return _signed_get("/v5/crypto-loan-fixed/renew-info", params)


@mcp.tool()
def new_crypto_loan_fixed_repay(loan_id: str = "", loan_currency: str = "") -> Any:
    """
    Fully repay a fixed crypto loan.

    Args:
        loan_id: Loan ID (either loan_id or loan_currency required).
        loan_currency: Loan currency.
    """
    params: dict[str, str] = {}
    if loan_id:
        params["loanId"] = loan_id
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_post("/v5/crypto-loan-fixed/fully-repay", params)


@mcp.tool()
def new_crypto_loan_fixed_repay_collateral(loan_currency: str, collateral_coin: str, amount: str, loan_id: str = "") -> Any:
    """
    Repay fixed crypto loan with collateral.

    Args:
        loan_currency: Loan currency.
        collateral_coin: Collateral coin.
        amount: Repay amount.
        loan_id: Loan ID (optional).
    """
    params: dict[str, str] = {
        "loanCurrency": loan_currency, "collateralCoin": collateral_coin, "amount": amount,
    }
    if loan_id:
        params["loanId"] = loan_id
    return _signed_post("/v5/crypto-loan-fixed/repay-collateral", params)


@mcp.tool()
def get_new_crypto_loan_fixed_repay_history(loan_currency: str = "", limit: int = 50) -> Any:
    """
    Get fixed crypto loan repayment history.

    Args:
        loan_currency: Filter by loan currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_get("/v5/crypto-loan-fixed/repayment-history", params)


@mcp.tool()
def new_crypto_loan_fixed_supply(order_currency: str, order_amount: str, annual_rate: str, term: str) -> Any:
    """
    Create a fixed crypto loan supply (lending) order.

    Args:
        order_currency: Supply currency.
        order_amount: Supply amount.
        annual_rate: Annual interest rate.
        term: Supply term in days.
    """
    return _signed_post("/v5/crypto-loan-fixed/supply", {
        "orderCurrency": order_currency, "orderAmount": order_amount,
        "annualRate": annual_rate, "term": term,
    })


@mcp.tool()
def get_new_crypto_loan_fixed_supply_contract(supply_currency: str = "", limit: int = 50) -> Any:
    """
    Get fixed crypto loan supply contract info.

    Args:
        supply_currency: Filter by currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if supply_currency:
        params["supplyCurrency"] = supply_currency
    return _signed_get("/v5/crypto-loan-fixed/supply-contract-info", params)


@mcp.tool()
def get_new_crypto_loan_fixed_supply_market(order_currency: str, order_by: str) -> Any:
    """
    Get fixed crypto loan lending market quotes.

    Args:
        order_currency: Supply currency.
        order_by: Order by field.
    """
    return _signed_get("/v5/crypto-loan-fixed/supply-order-quote", {
        "orderCurrency": order_currency, "orderBy": order_by,
    })


@mcp.tool()
def get_new_crypto_loan_fixed_supply_order(order_currency: str = "", limit: int = 50) -> Any:
    """
    Get fixed crypto loan supply order info.

    Args:
        order_currency: Filter by currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if order_currency:
        params["orderCurrency"] = order_currency
    return _signed_get("/v5/crypto-loan-fixed/supply-order-info", params)


# --- New Crypto Loan (Flexible) ---

@mcp.tool()
def new_crypto_loan_flexible_borrow(loan_currency: str, loan_amount: str) -> Any:
    """
    Borrow via flexible crypto loan.

    Args:
        loan_currency: Loan currency.
        loan_amount: Loan amount.
    """
    return _signed_post("/v5/crypto-loan-flexible/borrow", {
        "loanCurrency": loan_currency, "loanAmount": loan_amount,
    })


@mcp.tool()
def get_new_crypto_loan_flexible_borrow_history(loan_currency: str = "", limit: int = 50) -> Any:
    """
    Get flexible crypto loan borrowing history.

    Args:
        loan_currency: Filter by loan currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_get("/v5/crypto-loan-flexible/borrow-history", params)


@mcp.tool()
def new_crypto_loan_flexible_repay(loan_currency: str, amount: str) -> Any:
    """
    Repay a flexible crypto loan.

    Args:
        loan_currency: Loan currency.
        amount: Repay amount.
    """
    return _signed_post("/v5/crypto-loan-flexible/repay", {
        "loanCurrency": loan_currency, "amount": amount,
    })


@mcp.tool()
def new_crypto_loan_flexible_repay_collateral(loan_currency: str, collateral_coin: str, amount: str) -> Any:
    """
    Repay flexible crypto loan with collateral.

    Args:
        loan_currency: Loan currency.
        collateral_coin: Collateral coin.
        amount: Repay amount.
    """
    return _signed_post("/v5/crypto-loan-flexible/repay-collateral", {
        "loanCurrency": loan_currency, "collateralCoin": collateral_coin, "amount": amount,
    })


@mcp.tool()
def get_new_crypto_loan_flexible_repay_history(loan_currency: str = "", limit: int = 50) -> Any:
    """
    Get flexible crypto loan repayment history.

    Args:
        loan_currency: Filter by loan currency (optional).
        limit: Number of records (default: 50).
    """
    params: dict[str, str] = {"limit": str(limit)}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_get("/v5/crypto-loan-flexible/repayment-history", params)


@mcp.tool()
def get_new_crypto_loan_flexible_loans(loan_currency: str = "") -> Any:
    """
    Get ongoing flexible crypto loans.

    Args:
        loan_currency: Filter by loan currency (optional).
    """
    params: dict[str, str] = {}
    if loan_currency:
        params["loanCurrency"] = loan_currency
    return _signed_get("/v5/crypto-loan-flexible/ongoing-coin", params)
