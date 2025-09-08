# tests/test_client.py
import httpx
import respx

from demo_client import DemoClient, fetch_url


@respx.mock
def test_fetch_url_json():
    respx.get("https://api.example.com/json").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    out = fetch_url("https://api.example.com/json", 5.0)
    assert out["ok"] is True and out["status"] == 200 and out["data"]["ok"] is True


@respx.mock
def test_fetch_url_text():
    respx.get("https://api.example.com/plain").mock(return_value=httpx.Response(200, text="hello"))
    out = fetch_url("https://api.example.com/plain", 5.0)
    assert out["ok"] is True and out["text"] == "hello"


@respx.mock
def test_client_retry_then_ok():
    calls = {"n": 0}

    def handler(_request):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(503, text="busy")  # triggert Retry
        return httpx.Response(200, json=[{"id": 1}])

    respx.get("https://api.example.com/items").mock(side_effect=handler)

    with DemoClient("https://api.example.com", timeout=5.0) as c:
        data = c.get("/items")
        assert isinstance(data, list) and data[0]["id"] == 1
        assert calls["n"] == 2  # einmal 503, dann 200


@respx.mock
def test_fetch_url_error():
    respx.get("https://api.example.com/error").mock(return_value=httpx.Response(503, text="oops"))
    out = fetch_url("https://api.example.com/error", 5.0)
    assert out["ok"] is False and "error" in out
