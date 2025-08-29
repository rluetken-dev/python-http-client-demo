import json
import argparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from colorama import Fore, init

init(autoreset=True)  # Farben nach jeder Ausgabe zurücksetzen


def fetch(url: str, timeout: float):
    try:
        # Session mit Retry-Logik
        session = requests.Session()
        retry = Retry(
            total=3,                # bis zu 3 Versuche
            backoff_factor=0.5,     # 0.5s, 1s, 2s Wartezeit
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
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
    p = argparse.ArgumentParser(
        description="Kleiner HTTP-Client: holt eine URL und zeigt JSON schön formatiert an."
    )
    p.add_argument("--url", "-u", default="https://httpbin.org/get", help="Ziel-URL")
    p.add_argument("--timeout", "-t", type=float, default=5.0, help="Timeout in Sekunden")
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
