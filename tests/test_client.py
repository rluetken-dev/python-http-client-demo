import httpx
import respx

from demo_client import DemoClient, fetch_url


@respx.mock
def test_fetch_url_json_response() -> None:
    respx.get("https://api.example.com/json").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    result = fetch_url("https://api.example.com/json", timeout=5.0)

    assert result["ok"] is True
    assert result["status"] == 200
    assert result["data"] == {"ok": True}


@respx.mock
def test_fetch_url_text_response() -> None:
    respx.get("https://api.example.com/plain").mock(return_value=httpx.Response(200, text="hello"))

    result = fetch_url("https://api.example.com/plain", timeout=5.0)

    assert result["ok"] is True
    assert result["status"] == 200
    assert result["text"] == "hello"


@respx.mock
def test_demo_client_get_json_response() -> None:
    respx.get("https://api.example.com/items").mock(
        return_value=httpx.Response(200, json=[{"id": 1}])
    )

    with DemoClient("https://api.example.com", timeout=5.0) as client:
        data = client.get("/items")

    assert data == [{"id": 1}]


@respx.mock
def test_demo_client_post_json_response() -> None:
    respx.post("https://api.example.com/items").mock(
        return_value=httpx.Response(201, json={"id": 1, "name": "demo"})
    )

    with DemoClient("https://api.example.com", timeout=5.0) as client:
        data = client.post("/items", json={"name": "demo"})

    assert data == {"id": 1, "name": "demo"}


@respx.mock
def test_demo_client_retries_retryable_status_then_succeeds() -> None:
    calls = {"count": 0}

    def handler(_request: httpx.Request) -> httpx.Response:
        calls["count"] += 1

        if calls["count"] == 1:
            return httpx.Response(503, text="busy")

        return httpx.Response(200, json=[{"id": 1}])

    respx.get("https://api.example.com/items").mock(side_effect=handler)

    with DemoClient("https://api.example.com", timeout=5.0, retry_delay=0.0) as client:
        data = client.get("/items")

    assert data == [{"id": 1}]
    assert calls["count"] == 2


@respx.mock
def test_fetch_url_returns_error_for_http_error() -> None:
    respx.get("https://api.example.com/error").mock(return_value=httpx.Response(503, text="oops"))

    result = fetch_url("https://api.example.com/error", timeout=5.0)

    assert result["ok"] is False
    assert "error" in result
