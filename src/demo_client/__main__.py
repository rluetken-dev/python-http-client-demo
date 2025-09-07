from __future__ import annotations

import argparse
import sys

try:
    import httpx
except Exception:
    print(
        "Missing dep: install with `pip install httpx` (inside your venv).",
        file=sys.stderr,
    )
    raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="demo_client",
        description="Tiny HTTP client demo",
    )
    parser.add_argument(
        "method",
        nargs="?",
        default="get",
        choices=["get", "head", "post"],
        help="HTTP method",
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://httpbin.org/get",
        help="Request URL",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--data",
        help="POST data (raw string)",
    )
    args = parser.parse_args(argv)

    try:
        with httpx.Client(timeout=args.timeout) as client:
            resp = client.request(args.method.upper(), args.url, content=args.data)
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type', '')}")
        print("\n=== Body (first 800 chars) ===")
        print(resp.text[:800])
        return 0
    except httpx.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
