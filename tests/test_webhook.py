import hmac
import hashlib
from httpx import AsyncClient
from app.main import app
from app.config import settings

def sign(body: bytes):
    return hmac.new(settings.webhook_secret.encode(), body, hashlib.sha256).hexdigest()

async def test_valid_webhook_inserts(async_client: AsyncClient):
    body = b'{"message_id":"t1","from":"+911111111111","to":"+14155550100","ts":"2025-01-01T10:00:00Z","text":"hi"}'
    sig = sign(body)

    res = await async_client.post("/webhook", content=body, headers={"X-Signature": sig})
    assert res.status_code == 200

async def test_duplicate_is_idempotent(async_client: AsyncClient):
    body = b'{"message_id":"t2","from":"+911111111111","to":"+14155550100","ts":"2025-01-01T10:00:00Z","text":"hi"}'
    sig = sign(body)

    await async_client.post("/webhook", content=body, headers={"X-Signature": sig})
    res = await async_client.post("/webhook", content=body, headers={"X-Signature": sig})

    assert res.status_code == 200
