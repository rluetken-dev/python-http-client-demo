from demo_client import fetch


def test_fetch_bad_domain():
    # Invalid domain → network error expected
    res = fetch("https://does-not-exist.example.invalid", timeout=2)
    assert res.get("ok") is False
    assert "error" in res


def test_fetch_http_error_500():
    # 500 status → should return as an error
    res = fetch("https://httpbin.org/status/500", timeout=5)
    assert res.get("ok") is False
    assert "error" in res
