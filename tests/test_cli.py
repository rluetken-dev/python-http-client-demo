# tests/test_cli.py
import sys

import demo_client.__main__ as cli  # wir patchen das fetch_url im CLI-Modul


def test_cli_ok(monkeypatch, capsys):
    # Fake-HTTP: OK-Pfad
    monkeypatch.setattr(
        cli,
        "fetch_url",
        lambda url, timeout: {"ok": True, "status": 200, "data": {"hello": "world"}},
    )
    monkeypatch.setattr(sys, "argv", ["python", "--url", "https://example.com", "--timeout", "0.1"])
    cli.main()
    out = capsys.readouterr().out
    assert '"ok": true' in out.lower()  # JSON-Ausgabe vorhanden


def test_cli_error(monkeypatch, capsys):
    # Fake-HTTP: Fehlerpfad
    monkeypatch.setattr(cli, "fetch_url", lambda url, timeout: {"ok": False, "error": "boom"})
    monkeypatch.setattr(sys, "argv", ["python", "--url", "https://example.com"])
    cli.main()
    out = capsys.readouterr().out
    assert "boom" in out
