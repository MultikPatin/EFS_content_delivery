from logging import Logger

from elasticsearch import AsyncElasticsearch

from src.api.db import AbstractDBClient


class ElasticDB(AbstractDBClient):
    """Клиент для работы api с Elastic."""

    __es: AsyncElasticsearch
    __logger: Logger

    def __init__(self, es: AsyncElasticsearch, logger: Logger):
        self.__es = es
        self.__logger = logger

    async def get_by_id(self, obj_id: str, **kwargs) -> dict | None:
        index = self.__validate_index(kwargs.get("index"))
        if not index:
            return None
        pass

    async def get_all(
        self, page_number: int, page_size: int, **kwargs
    ) -> list[dict] | None:
        index = self.__validate_index(kwargs.get("index"))
        if not index:
            return None
        pass

    async def get_search_by_query(
        self, page_number: int, page_size: int, field: str, query: str, **kwargs
    ) -> list[dict] | None:
        index = self.__validate_index(kwargs.get("index"))
        if not index:
            return None
        pass

    async def __validate_index(self, index: str):
        index_list = await self.__es.indices.get("*")
        if index not in index_list:
            return index
        else:
            self.__logger.error(
                "A nonexistent index '%s' was passed.",
                index,
            )
            return None

    async def close(self):
        """
        Закрыть соединение с Elastic.

        """
        await self.__es.close()
        self.__logger.info("Connection to Elastic was closed.")

    async def ping(self) -> bool:
        """
        Ping the Elastic server to ensure the connection is still alive.

        Returns:
            bool: True if the ping was successful, False if it failed.
        """
        return await self.__es.ping()


elastic: ElasticDB | None = None


async def get_elastic() -> ElasticDB:
    return elastic
