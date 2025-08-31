import json
import argparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from colorama import Fore, init


init(autoreset=True)  # Colors reset after every output


def fetch(url: str, timeout: float):
    try:
        # Session with retry-logic
        session = requests.Session()
        retry = Retry(
            total=3,  # up to 3 trys
            backoff_factor=0.5,  # 0.5s, 1s, 2s waiting time
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=[
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "HEAD",
                "OPTIONS",
                "PATCH",
            ],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        r = session.get(url, timeout=timeout)
        r.raise_for_status()
        try:
            return {"ok": True, "status": r.status_code, "data": r.json()}
        except ValueError:
            return {"ok": True, "status": r.status_code, "text": r.text}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e), "url": url}


def parse_args():
    p = argparse.ArgumentParser(description="My HTTP-client (SSH-Test commit)")
    p.add_argument("--url", "-u", default="https://httpbin.org/get", help="Target-URL")
    p.add_argument(
        "--timeout", "-t", type=float, default=5.0, help="Timeout in seconds"
    )
    return p.parse_args()


def main():
    args = parse_args()
    result = fetch(args.url, args.timeout)

    if result.get("ok"):
        print(Fore.GREEN + json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(Fore.RED + json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
