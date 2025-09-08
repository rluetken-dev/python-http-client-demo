import httpx
import respx

from demo_client import DemoClient


@respx.mock
def test_get_ok():
    respx.get("https://api.example.com/items").mock(
        return_value=httpx.Response(200, json=[{"id": 1}])
    )
    with DemoClient("https://api.example.com") as c:
        data = c.get("/items")
        assert isinstance(data, list)
        assert data[0]["id"] == 1
