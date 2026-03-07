from typing import Any

from src import mcp
from src.client import _public_get


@mcp.tool()
def get_announcement(locale: str = "en-US", limit: int = 20) -> Any:
    """
    Get Bybit announcements.

    Args:
        locale: Language locale, e.g., en-US, zh-CN, zh-TW, ja-JP, ko-KR.
        limit: Number of records (default: 20).
    """
    return _public_get("/v5/announcements/index", {"locale": locale, "limit": str(limit)})


@mcp.tool()
def get_system_status() -> Any:
    """Get Bybit system/platform status."""
    return _public_get("/v5/system/status", {})
