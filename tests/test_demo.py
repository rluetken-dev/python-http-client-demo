# --- CLI tests for demo_client.__main__ ---

import httpx
import pytest

import demo_client.__main__ as cli


class DummyTransport(httpx.BaseTransport):
    def handle_request(self, request):
        return httpx.Response(
            200,
            json={"ok": True, "url": str(request.url), "method": request.method},
            headers={"content-type": "application/json"},
        )


def _patched_client(timeout: float) -> httpx.Client:
    # nutzt unseren DummyTransport statt echter Netzwerkaufrufe
    return httpx.Client(transport=DummyTransport(), timeout=timeout)


def test_cli_help_exits():
    # argparse beendet bei --help mit SystemExit(0)
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
    assert "application/json" in out


def test_cli_http_error(monkeypatch, capsys):
    class Boom:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def request(self, *a, **kw):
            raise httpx.HTTPError("boom")

    monkeypatch.setattr(httpx, "Client", lambda timeout: Boom())
    rc = cli.main(["get", "https://example.com"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "HTTP error:" in err
