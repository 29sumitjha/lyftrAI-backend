import hmac
import hashlib
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .config import get_settings
from .models import init_db
from .storage import *
from .logging_utils import logging_middleware
from .metrics import *

app = FastAPI()

settings = get_settings()

app.middleware("http")(logging_middleware)


class WebhookMessage(BaseModel):
    message_id: str
    from_: str = Field(alias="from")
    to: str
    ts: str
    text: str | None = None
    
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("from_", "to")
    def check_e164(cls, v):
        if not v.startswith("+") or not v[1:].isdigit():
            raise ValueError("must be E.164-like (+ then digits)")
        return v

    @field_validator("ts")
    def check_ts(cls, v):
        if not v.endswith("Z"):
            raise ValueError("must be UTC ISO8601 ending with Z")
        return v


@app.on_event("startup")
async def startup():
    await init_db()


def verify_signature(secret: str, body: bytes, signature: str) -> bool:
    mac = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)


@app.post("/webhook")
async def webhook(request: Request):
    raw = await request.body()
    sig = request.headers.get("X-Signature")

    if not sig or not verify_signature(settings.webhook_secret, raw, sig):
        webhook_outcomes["invalid_signature"] += 1
        raise HTTPException(status_code=401, detail="invalid signature")

    try:
        msg = WebhookMessage.model_validate_json(raw)
    except Exception:
        webhook_outcomes["validation_error"] += 1
        raise HTTPException(status_code=422, detail="validation error")

    dup = await message_exists(msg.message_id)

    if not dup:
        await insert_message(
            {
                "message_id": msg.message_id,
                "from_msisdn": msg.from_,
                "to_msisdn": msg.to,
                "ts": msg.ts,
                "text": msg.text,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        )
        webhook_outcomes["created"] += 1
    else:
        webhook_outcomes["duplicate"] += 1

    return {"status": "ok"}


@app.get("/messages")
async def get_messages(limit: int = 50, offset: int = 0,
                       from_: str | None = None,
                       since: str | None = None,
                       q: str | None = None):

    limit = max(1, min(limit, 100))
    offset = max(offset, 0)

    total, data = await list_messages(limit, offset, from_, since, q)

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@app.get("/stats")
async def get_stats():
    return await stats()


@app.get("/health/live")
async def live():
    return {"status": "live"}


@app.get("/health/ready")
async def ready():
    if not settings.webhook_secret:
        raise HTTPException(status_code=503, detail="secret missing")

    await init_db()
    return {"status": "ready"}


@app.get("/metrics")
async def metrics():
    return PlainTextResponse(render_metrics(), status_code=200)
