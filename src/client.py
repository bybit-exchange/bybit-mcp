import logging
import time
import hmac
import hashlib
import json
import requests

logger = logging.getLogger("bybit-mcp")


class Config:
    api_key: str = ""
    secret_key: str = ""
    base_url: str = "https://api.bybit.com"
    recv_window: str = "5000"

    def configure(self, api_key: str, secret_key: str, testnet: bool = False):
        self.api_key = api_key or ""
        self.secret_key = secret_key or ""
        if testnet:
            self.base_url = "https://api-testnet.bybit.com"

    @property
    def has_credentials(self) -> bool:
        return bool(self.api_key and self.secret_key)


config = Config()


def _sign_request(timestamp: str, params: str) -> str:
    """Generate HMAC-SHA256 signature for Bybit V5 API."""
    param_str = f"{timestamp}{config.api_key}{config.recv_window}{params}"
    return hmac.new(
        config.secret_key.encode("utf-8"),
        param_str.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _auth_headers(timestamp: str, signature: str) -> dict:
    """Build authenticated request headers."""
    return {
        "X-BAPI-API-KEY": config.api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-SIGN-TYPE": "2",
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": config.recv_window,
        "Content-Type": "application/json",
    }


def _require_credentials():
    """Raise a clear error if API credentials are not configured."""
    if not config.has_credentials:
        return {
            "error": "API credentials not configured. "
            "Set BYBIT_API_KEY and BYBIT_SECRET_KEY via .env file or command-line arguments."
        }
    return None


def _public_get(endpoint: str, params: dict) -> dict:
    """Make an unauthenticated GET request to Bybit V5 API."""
    logger.debug("PUBLIC GET %s params=%s", endpoint, params)
    try:
        response = requests.get(f"{config.base_url}{endpoint}", params=params)
        data = response.json()
    except requests.RequestException as e:
        logger.error("PUBLIC GET %s failed: %s", endpoint, e)
        return {"error": f"Request failed: {e}"}
    if data.get("retCode") == 0:
        logger.debug("PUBLIC GET %s success", endpoint)
        return data.get("result", {})
    logger.warning("PUBLIC GET %s retCode=%s retMsg=%s", endpoint, data.get("retCode"), data.get("retMsg"))
    return {"error": data.get("retMsg", "Unknown error"), "retCode": data.get("retCode")}


def _signed_get(endpoint: str, params: dict) -> dict:
    """Make a signed GET request to Bybit V5 API."""
    cred_error = _require_credentials()
    if cred_error:
        return cred_error
    logger.debug("SIGNED GET %s params=%s", endpoint, params)
    timestamp = str(int(time.time() * 1000))
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = _sign_request(timestamp, query_string)
    headers = _auth_headers(timestamp, signature)
    try:
        response = requests.get(f"{config.base_url}{endpoint}", headers=headers, params=params)
        data = response.json()
    except requests.RequestException as e:
        logger.error("SIGNED GET %s failed: %s", endpoint, e)
        return {"error": f"Request failed: {e}"}
    if data.get("retCode") == 0:
        logger.debug("SIGNED GET %s success", endpoint)
        return data.get("result", {})
    logger.warning("SIGNED GET %s retCode=%s retMsg=%s", endpoint, data.get("retCode"), data.get("retMsg"))
    return {"error": data.get("retMsg", "Unknown error"), "retCode": data.get("retCode")}


def _signed_post(endpoint: str, params: dict) -> dict:
    """Make a signed POST request to Bybit V5 API."""
    cred_error = _require_credentials()
    if cred_error:
        return cred_error
    logger.debug("SIGNED POST %s params=%s", endpoint, params)
    timestamp = str(int(time.time() * 1000))
    body = json.dumps(params)
    signature = _sign_request(timestamp, body)
    headers = _auth_headers(timestamp, signature)
    try:
        response = requests.post(f"{config.base_url}{endpoint}", headers=headers, data=body)
        data = response.json()
    except requests.RequestException as e:
        logger.error("SIGNED POST %s failed: %s", endpoint, e)
        return {"error": f"Request failed: {e}"}
    if data.get("retCode") == 0:
        logger.debug("SIGNED POST %s success", endpoint)
        return data.get("result", {})
    logger.warning("SIGNED POST %s retCode=%s retMsg=%s", endpoint, data.get("retCode"), data.get("retMsg"))
    return {"error": data.get("retMsg", "Unknown error"), "retCode": data.get("retCode")}
