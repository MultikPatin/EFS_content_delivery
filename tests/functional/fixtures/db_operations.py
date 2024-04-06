from typing import Any

import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import settings

from redis.asyncio import Redis


def get_es_bulk_query(data, index, id):
    bulk_query = []
    for row in data:
        doc = {"_index": index, "_id": row[id]}
        doc.update({"_source": row})
        bulk_query.append(doc)
    return bulk_query


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
        await redis_client.flushdb(asynchronous=True)

    return inner
