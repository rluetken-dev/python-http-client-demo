import argparse
import json

from colorama import Fore, init

from demo_client import fetch_url

init(autoreset=True)  # Farben nach jeder Ausgabe zurücksetzen


def parse_args():
    p = argparse.ArgumentParser(description="HTTP client (httpx)")
    p.add_argument("--url", "-u", default="https://httpbin.org/get", help="Target URL")
    p.add_argument("--timeout", "-t", type=float, default=5.0, help="Timeout (s)")
    return p.parse_args()


def main():
    args = parse_args()
    result = fetch_url(args.url, args.timeout)
    pretty = json.dumps(result, indent=2, ensure_ascii=False)
    print((Fore.GREEN if result.get("ok") else Fore.RED) + pretty)


if __name__ == "__main__":
    main()
