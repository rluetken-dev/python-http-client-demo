from __future__ import annotations

import time
from typing import Any, Optional

import httpx

DEFAULT_HEADERS = {"User-Agent": "python-http-client-demo/1.0"}
RETRY_STATUS = {429, 500, 502, 503, 504}


class DemoClient:
    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=DEFAULT_HEADERS,
            # http2=True,  # optional: nur aktivieren, wenn 'h2' installiert ist
        )

    def _request_with_retry(self, method: str, path: str, **kwargs) -> httpx.Response:
        retries = 3
        backoff = 0.5
        last_exc: Optional[Exception] = None

        for attempt in range(retries):
            try:
                resp = self._client.request(method, path, **kwargs)
                if resp.status_code in RETRY_STATUS:

                    raise httpx.HTTPStatusError(
                        "retryable status",
                        request=resp.request,
                        response=resp,
                    )
                return resp
            except (httpx.TransportError, httpx.HTTPStatusError) as e:
                last_exc = e
                if attempt < retries - 1:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    break

        if last_exc:
            raise last_exc
        raise RuntimeError("Request failed without an exception")

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        resp = self._request_with_retry("GET", path, params=params)
        resp.raise_for_status()
        ctype = resp.headers.get("content-type", "").lower()
        return resp.json() if "application/json" in ctype else resp.text

    def post(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        resp = self._request_with_retry("POST", path, json=json)
        resp.raise_for_status()
        ctype = resp.headers.get("content-type", "").lower()
        return resp.json() if "application/json" in ctype else resp.text

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "DemoClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def fetch_url(url: str, timeout: float = 5.0) -> dict[str, Any]:
    """Convenience für CLI: komplette URL aufrufen."""
    try:
        with httpx.Client(timeout=timeout, headers=DEFAULT_HEADERS) as c:
            r = c.get(url)
            r.raise_for_status()
            ctype = r.headers.get("content-type", "").lower()
            if "application/json" in ctype:
                return {"ok": True, "status": r.status_code, "data": r.json()}
            return {"ok": True, "status": r.status_code, "text": r.text}
    except httpx.HTTPError as e:
        return {"ok": False, "error": str(e), "url": url}


# Backcompat für Tests: tests importieren noch `fetch`
def fetch(url: str, timeout: float) -> dict[str, Any]:
    return fetch_url(url, timeout)
