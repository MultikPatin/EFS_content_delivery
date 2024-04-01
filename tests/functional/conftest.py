import asyncio

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import aiohttp

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def get_es_bulk_query(data, index, id):
    bulk_query: list[dict] = []
    for row in data:
        doc = {"_index": "movies", "_id": row["uuid"]}
        doc.update({"_source": row})
        bulk_query.append(doc)
    return bulk_query


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        bulk_query = get_es_bulk_query(
            data, test_settings.es_index, test_settings.es_id_field
        )
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(
            index=test_settings.es_index,
            settings=test_settings.es_index_settings,
            mappings=test_settings.es_index_mapping,
        )

        _, errors = await async_bulk(
            es_client, actions=bulk_query, refresh="wait_for"
        )

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner

@pytest_asyncio.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def make_get_request(session):
    async def inner(path: str, query_data: dict):
        url = test_settings.service_url + "/api/v1" + path
        async with session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status

        return body, status
    return inner
