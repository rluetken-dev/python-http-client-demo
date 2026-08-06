import httpx
import respx

from demo_client import fetch_url


@respx.mock
def test_fetch_url_returns_error_for_http_500() -> None:
    respx.get("https://api.example.com/error").mock(
        return_value=httpx.Response(500, text="server error")
    )

    result = fetch_url("https://api.example.com/error", timeout=5.0)

    assert result["ok"] is False
    assert "error" in result
    assert result["url"] == "https://api.example.com/error"


@respx.mock
def test_fetch_url_returns_error_for_transport_failure() -> None:
    respx.get("https://api.example.com/unreachable").mock(
        side_effect=httpx.ConnectError("connection failed")
    )

    result = fetch_url("https://api.example.com/unreachable", timeout=5.0)

    assert result["ok"] is False
    assert "connection failed" in result["error"]
    assert result["url"] == "https://api.example.com/unreachable"
