from logging import Logger

from elasticsearch import AsyncElasticsearch, NotFoundError

from src.api.db import AbstractDBClient


class ElasticDB(AbstractDBClient):
    """Клиент для работы api с Elastic."""

    __es: AsyncElasticsearch
    __logger: Logger

    def __init__(self, es: AsyncElasticsearch, logger: Logger):
        """Инициализация экземпляра класса.

        Args:
            es (AsyncElasticsearch): экземпляр класса AsyncElasticsearch
            logger (Logger): экземпляр класса Logger
        """
        self.__es = es
        self.__logger = logger

    async def get_by_id(self, obj_id: str, **kwargs) -> dict | None:
        """Получить объект по его идентификатору.

        Args:
            obj_id (str): идентификатор объекта
            **kwargs: дополнительные параметры запроса

        Returns:
            dict | None: возвращает объект в формате JSON или None, если объект не найден
        """
        index = kwargs.get("index")
        await self.__validate_index(index)
        try:
            data = await self.__es.get(index=index, id=obj_id)
        except (NotFoundError, ConnectionError):
            return None
        return data["_source"]

    async def get_all(
        self, page_number: int, page_size: int, **kwargs
    ) -> list[dict] | None:
        """Получить все объекты.

        Args:
            page_number (int): номер страницы
            page_size (int): количество объектов на странице
            **kwargs: дополнительные параметры запроса

        Returns:
            list[dict] | None: возвращает список объектов в формате JSON или None, если объектов нет
        """
        index = kwargs.get("index")
        await self.__validate_index(index)
        try:
            docs = await self.__es.search(
                index=index,
                filter_path=kwargs.get("filter_path"),
                query=kwargs.get("query"),
                from_=page_number,
                size=page_size,
                sort=kwargs.get("sort"),
            )
        except (NotFoundError, ConnectionError):
            return None
        return docs["hits"]["hits"]

    async def get_search_by_query(
        self, page_number: int, page_size: int, field: str, query: str, **kwargs
    ) -> list[dict] | None:
        """Получить объекты по поисковому запросу.

        Args:
            page_number (int): номер страницы
            page_size (int): количество объектов на странице
            field (str): имя поля для поиска
            query (str): поисковый запрос
            **kwargs: дополнительные параметры запроса

        Returns:
            list[dict] | None: возвращает список объектов в формате JSON или None, если объектов нет
        """
        index = kwargs.get("index")
        await self.__validate_index(index)
        if query:
            body = {"match": {field: {"query": query, "fuzziness": "auto"}}}
        else:
            body = None
        try:
            docs = await self.__es.search(
                index=index,
                filter_path="hits.hits._source",
                query=body,
                from_=page_number,
                size=page_size,
                sort=kwargs.get("sort"),
            )
        except (NotFoundError, ConnectionError):
            return None
        if not docs:
            return None
        return docs["hits"]["hits"]

    async def __validate_index(self, index: str):
        """Проверить, что индекс существует.

        Args:
            index (str): имя индекса

        Raises:
            ValueError: если индекс не существует

        Returns:
            str: возвращает имя индекса
        """
        return index

    async def close(self):
        """Закрыть соединение с Elastic."""
        await self.__es.close()
        self.__logger.info("Connection to Elastic was closed.")

    async def ping(self) -> bool:
        """Проверить соединение с Elastic.

        Returns:
            bool: возвращает True, если соединение установлено, и False в противном случае
        """
        return await self.__es.ping()


elastic: ElasticDB | None = None


async def get_elastic() -> ElasticDB:
    return elastic
