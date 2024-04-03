import asyncio
from typing import Any

import json
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import aiohttp

from tests.functional.settings import settings

from redis.asyncio import Redis


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def get_es_bulk_query(data, index, id):
    bulk_query = []
    for row in data:
        doc = {"_index": index, "_id": row[id]}
        doc.update({"_source": row})
        bulk_query.append(doc)
    return bulk_query


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=settings.get_es_host, verify_certs=False)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    client = Redis(**settings.get_redis_host)
    # print(f"\n\n\n{settings.get_redis_host}\n\n\n\n")
    yield client
    await client.aclose()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict[str, Any]], module: str):
        index_data = settings.es_index_data[module]
        bulk_query = get_es_bulk_query(
            data, index_data["name"], settings.es_id_field
        )
        if await es_client.indices.exists(index=index_data["name"]):
            await es_client.indices.delete(index=index_data["name"])
        await es_client.indices.create(
            index=index_data["name"],
            settings=index_data["settings"],
            mappings=index_data["mappings"],
        )

        _, errors = await async_bulk(
            es_client, actions=bulk_query, refresh="wait_for"
        )
        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def es_delete_data(es_client: AsyncElasticsearch):
    async def inner(module: str):
        index_data = settings.es_index_data[module]

        if await es_client.indices.exists(index=index_data["name"]):
            await es_client.indices.delete(index=index_data["name"])

    return inner


@pytest.fixture
def clear_cache(redis_client: Redis):
    async def inner():
        print(f"CACHE BEFORE DEL: {await redis_client.scan()}")
        await redis_client.flushdb(asynchronous=True)

    return inner


@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(path: str, query_data: dict = None):
        url = settings.get_api_host + "/api/v1" + path
        try:
            async with session.get(url, params=query_data) as response:
                body = await response.read()
            body = json.loads(body)
            status = response.status
        finally:
            return body, status

    return inner
