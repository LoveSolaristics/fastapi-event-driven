from asyncio import get_event_loop_policy

import pytest
from httpx import AsyncClient
from redis import Redis

from delivery_hub.app import app
from delivery_hub.db.connection import redis


pytest_plugins: list[str] = []


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def redis_connection() -> Redis:
    """
    Create connection
    """
    return redis


@pytest.fixture
async def client(redis_connection: Redis):
    """
    Returns a client that can be used to interact with the application.
    """
    yield AsyncClient(app=app, base_url="http://test")
