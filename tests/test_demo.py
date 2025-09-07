import httpx
import pytest

import demo_client.__main__ as cli
from demo_client import fetch


# --- bestehender Netzwerktest (behalten) ---
def test_fetch_httpbin_uuid():
    result = fetch("https://httpbin.org/uuid", timeout=5)
    assert result.get("ok") is True
    # Result can be "data" (JSON) or "text" - check for at least one
    assert ("data" in result and "uuid" in result["data"]) or (
        "text" in result and "uuid" in result["text"]
    )


# --- fetch tests (netzwerkbasiert über httpbin, robust) ---
def test_fetch_ok_json_network():
    result = fetch("https://httpbin.org/json", timeout=5)
    assert result.get("status") == 200
    # Inhalt muss ankommen – egal ob als data (dict) oder text (str)
    assert ("data" in result and isinstance(result["data"], dict)) or ("text" in result)


def test_fetch_error_status_network():
    result = fetch("https://httpbin.org/status/500", timeout=5)
    # Bei Fehlern akzeptieren wir beide Varianten:
    # - status >= 400 ODER
    # - ok == False und ein error-Feld ist vorhanden
    assert (result.get("status", 0) >= 400) or (
        result.get("ok") is False and "error" in result
    )


# --- CLI tests für demo_client.__main__ (netzwerkfrei) ---

# Original-Client sichern, bevor wir patchen
_ORIG_CLIENT = httpx.Client


class DummyTransport(httpx.BaseTransport):
    def handle_request(self, request):
        return httpx.Response(
            200,
            json={"ok": True, "url": str(request.url), "method": request.method},
            headers={"content-type": "application/json"},
        )


def _patched_client(*args, **kwargs) -> httpx.Client:
    # ORIGINALEN Client nutzen, sonst rekursive Aufrufe
    kwargs["transport"] = DummyTransport()
    return _ORIG_CLIENT(*args, **kwargs)


def test_cli_help_exits():
    with pytest.raises(SystemExit) as e:
        cli.main(["--help"])
    assert e.value.code == 0


def test_cli_get(monkeypatch, capsys):
    monkeypatch.setattr(httpx, "Client", _patched_client)
    rc = cli.main(["get", "https://example.com"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Status: 200" in out
    assert "application/json" in out
    assert "https://example.com" in out


def test_cli_head(monkeypatch, capsys):
    monkeypatch.setattr(httpx, "Client", _patched_client)
    rc = cli.main(["head", "https://example.com"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Status: 200" in out


def test_cli_post_data(monkeypatch, capsys):
    monkeypatch.setattr(httpx, "Client", _patched_client)
    rc = cli.main(["post", "https://example.com/post", "--data", "hello"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Status: 200" in out


def test_cli_http_error(monkeypatch, capsys):
    class Boom:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def request(self, *a, **kw):
            raise httpx.HTTPError("boom")

    monkeypatch.setattr(httpx, "Client", lambda *a, **kw: Boom())
    rc = cli.main(["get", "https://example.com"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "HTTP error:" in err
