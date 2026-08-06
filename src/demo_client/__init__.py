from __future__ import annotations

import time
from typing import Any

import httpx

DEFAULT_HEADERS = {"User-Agent": "python-http-client-demo/1.0"}
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}


class DemoClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        retries: int = 3,
        retry_delay: float = 0.5,
    ) -> None:
        self._retries = retries
        self._retry_delay = retry_delay
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=DEFAULT_HEADERS,
        )

    def _request_with_retry(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        last_error: Exception | None = None
        delay = self._retry_delay

        for attempt in range(self._retries):
            try:
                response = self._client.request(method, path, **kwargs)

                if response.status_code not in RETRY_STATUS_CODES:
                    return response

                raise httpx.HTTPStatusError(
                    "Retryable HTTP status",
                    request=response.request,
                    response=response,
                )
            except (httpx.TransportError, httpx.HTTPStatusError) as error:
                last_error = error

                if attempt < self._retries - 1:
                    time.sleep(delay)
                    delay *= 2

        if last_error is not None:
            raise last_error

        raise RuntimeError("Request failed without an exception")

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self._request_with_retry("GET", path, params=params)
        response.raise_for_status()
        return parse_response(response)

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        response = self._request_with_retry("POST", path, json=json)
        response.raise_for_status()
        return parse_response(response)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> DemoClient:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()


def parse_response(response: httpx.Response) -> Any:
    content_type = response.headers.get("content-type", "").lower()
    return response.json() if "application/json" in content_type else response.text


def fetch_url(url: str, timeout: float = 5.0) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=timeout, headers=DEFAULT_HEADERS) as client:
            response = client.get(url)
            response.raise_for_status()

            result: dict[str, Any] = {
                "ok": True,
                "status": response.status_code,
            }

            if "application/json" in response.headers.get("content-type", "").lower():
                result["data"] = response.json()
            else:
                result["text"] = response.text

            return result
    except httpx.HTTPError as error:
        return {
            "ok": False,
            "error": str(error),
            "url": url,
        }


def fetch(url: str, timeout: float) -> dict[str, Any]:
    return fetch_url(url, timeout)
