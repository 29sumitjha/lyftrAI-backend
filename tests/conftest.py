import os
import sys
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# --- FIX PATH BEFORE ANY IMPORTS ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app
from app.models import init_db


@pytest_asyncio.fixture
async def async_client():
    # create tables for tests
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

