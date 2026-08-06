from __future__ import annotations

import argparse
import json
from typing import Any

from colorama import Fore, init

from demo_client import fetch_url

DEFAULT_URL = "https://httpbin.org/get"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo HTTP client powered by httpx")
    parser.add_argument(
        "--url",
        "-u",
        default=DEFAULT_URL,
        help=f"Target URL. Defaults to {DEFAULT_URL}",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=float,
        default=5.0,
        help="Request timeout in seconds. Defaults to 5.0",
    )
    return parser.parse_args()


def format_result(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False)


def main() -> None:
    init(autoreset=True)

    args = parse_args()
    result = fetch_url(args.url, args.timeout)
    color = Fore.GREEN if result.get("ok") else Fore.RED

    print(color + format_result(result))


if __name__ == "__main__":
    main()
