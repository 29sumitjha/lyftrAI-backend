from httpx import AsyncClient

async def test_stats(async_client: AsyncClient):
    res = await async_client.get("/stats")
    assert res.status_code == 200
    body = res.json()
    assert "total_messages" in body
