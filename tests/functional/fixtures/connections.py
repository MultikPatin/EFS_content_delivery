import asyncio

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings

from redis.asyncio import Redis
import aiohttp


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=settings.get_es_host, verify_certs=False)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    client = Redis(**settings.get_redis_host)
    yield client
    await client.aclose()


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
