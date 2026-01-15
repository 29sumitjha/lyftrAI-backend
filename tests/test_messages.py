from httpx import AsyncClient

async def test_messages_list(async_client: AsyncClient):
    res = await async_client.get("/messages")
    assert res.status_code == 200
    assert "data" in res.json()
