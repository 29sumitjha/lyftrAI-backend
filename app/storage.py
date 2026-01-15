from sqlalchemy import text
from .models import engine


async def insert_message(msg):
    query = text("""
        INSERT INTO messages(message_id, from_msisdn, to_msisdn, ts, text, created_at)
        VALUES (:message_id, :from_msisdn, :to_msisdn, :ts, :text, :created_at)
    """)

    async with engine.begin() as conn:
        await conn.execute(query, msg)


async def message_exists(message_id: str) -> bool:
    q = text("SELECT 1 FROM messages WHERE message_id=:message_id")

    async with engine.connect() as conn:
        res = await conn.execute(q, {"message_id": message_id})
        return res.scalar() is not None


async def list_messages(limit, offset, from_filter, since, q):
    base = "FROM messages WHERE 1=1 "
    params = {}

    if from_filter:
        base += "AND from_msisdn=:from_msisdn "
        params["from_msisdn"] = from_filter

    if since:
        base += "AND ts >= :since "
        params["since"] = since

    if q:
        base += "AND LOWER(text) LIKE LOWER(:q) "
        params["q"] = f"%{q}%"

    total_q = text("SELECT COUNT(*) " + base)

    data_q = text(
        "SELECT message_id, from_msisdn, to_msisdn, ts, text "
        + base
        + "ORDER BY ts ASC, message_id ASC "
        + "LIMIT :limit OFFSET :offset"
    )

    params["limit"] = limit
    params["offset"] = offset

    async with engine.connect() as conn:
        total = (await conn.execute(total_q, params)).scalar()
        rows = (await conn.execute(data_q, params)).fetchall()

    data = [dict(row._mapping) for row in rows]

    return total, data


async def stats():
    async with engine.connect() as conn:
        total = (await conn.execute(text("SELECT COUNT(*) FROM messages"))).scalar()

        senders = await conn.execute(text("""
            SELECT from_msisdn, COUNT(*) AS c
            FROM messages
            GROUP BY from_msisdn
            ORDER BY c DESC
            LIMIT 10
        """))

        first_ts = (await conn.execute(text("SELECT MIN(ts) FROM messages"))).scalar()
        last_ts = (await conn.execute(text("SELECT MAX(ts) FROM messages"))).scalar()

    return {
        "total_messages": total,
        "senders_count": len(list(senders)),
        "messages_per_sender": [
            {"from": r[0], "count": r[1]} for r in senders
        ],
        "first_message_ts": first_ts,
        "last_message_ts": last_ts
    }
