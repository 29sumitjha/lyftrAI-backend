from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text
from .config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(settings.database_url, echo=False)


CREATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
  message_id TEXT PRIMARY KEY,
  from_msisdn TEXT NOT NULL,
  to_msisdn   TEXT NOT NULL,
  ts          TEXT NOT NULL,
  text        TEXT,
  created_at  TEXT NOT NULL
);
"""


async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text(CREATE_SCHEMA))
