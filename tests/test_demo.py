from demo_client import fetch


def test_fetch_httpbin_uuid():
    result = fetch("https://httpbin.org/uuid", timeout=5)
    assert result.get("ok") is True
    # Result can be "data" (JSON) or "text" - check for at least one
    assert ("data" in result and "uuid" in result["data"]) or (
        "text" in result and "uuid" in result["text"]
    )
