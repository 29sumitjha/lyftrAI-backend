http_requests = {}
webhook_outcomes = {
    "created": 0,
    "duplicate": 0,
    "invalid_signature": 0,
    "validation_error": 0
}

latency_buckets = {"100": 0, "500": 0, "+Inf": 0}


def render_metrics():
    lines = []

    for (path, status), count in http_requests.items():
        lines.append(f'http_requests_total{{path="{path}",status="{status}"}} {count}')

    for res, count in webhook_outcomes.items():
        lines.append(f'webhook_requests_total{{result="{res}"}} {count}')

    for b, v in latency_buckets.items():
        lines.append(f'request_latency_ms_bucket{{le="{b}"}} {v}')

    return "\n".join(lines) + "\n"
