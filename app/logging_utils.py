import json
import time
import uuid
from datetime import datetime, timezone


def json_log(level, **kwargs):
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        **kwargs
    }
    print(json.dumps(payload), flush=True)


async def logging_middleware(request, call_next):
    start = time.time()
    request_id = str(uuid.uuid4())

    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        latency_ms = int((time.time() - start) * 1000)

        json_log(
            "INFO",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code if response else 500,
            latency_ms=latency_ms
        )
