import sys

import demo_client.__main__ as cli


def test_cli_prints_success_response(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        cli,
        "fetch_url",
        lambda url, timeout: {"ok": True, "status": 200, "data": {"hello": "world"}},
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["python", "--url", "https://example.com", "--timeout", "0.1"],
    )

    cli.main()

    output = capsys.readouterr().out
    assert '"ok": true' in output.lower()
    assert '"hello": "world"' in output


def test_cli_prints_error_response(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        cli,
        "fetch_url",
        lambda url, timeout: {"ok": False, "error": "boom"},
    )
    monkeypatch.setattr(sys, "argv", ["python", "--url", "https://example.com"])

    cli.main()

    output = capsys.readouterr().out
    assert '"ok": false' in output.lower()
    assert "boom" in output
