from elasticsearch import NotFoundError

from src.api.db.elastic import ApiElasticClient
from src.api.db.redis import ApiRedisClient


class BaseElasticService:
    def __init__(
        self,
        redis: ApiRedisClient,
        elastic_client: ApiElasticClient,
        cache_ex: int,
    ):
        self._redis = redis
        self._elastic_client = elastic_client
        self._cache_ex = cache_ex

    async def _get_data_from_elastic(
        self, index: str, doc_id: str
    ) -> dict | None:
        try:
            data = await self._elastic_client.get_async_client().get(
                index=index, id=doc_id
            )
        except NotFoundError:
            return None
        return data["_source"]

    async def _get_search_from_elastic(
        self,
        index: str,
        page_number: int,
        page_size: int,
        field: str,
        query: str,
    ) -> list[dict] | None:
        body = None
        if query:
            body = {"match": {field: {"query": query, "fuzziness": "auto"}}}
        try:
            docs = await self._elastic_client.get_async_client().search(
                index=index,
                filter_path="hits.hits._source",
                query=body,
                from_=page_number,
                size=page_size,
            )

            if not docs:
                return None
        except (NotFoundError, ConnectionError):
            return None
        return docs["hits"]["hits"]

    @staticmethod
    def _get_paginated_data(
        response,
        page_number: int,
        page_size: int,
    ):
        return response[(page_number - 1) * page_size : page_number * page_size]
