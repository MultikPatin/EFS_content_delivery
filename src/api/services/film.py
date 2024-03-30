from functools import lru_cache

from elastic_transport import ConnectionError
from elasticsearch import NotFoundError
from fastapi import Depends

from src.api.core.config import settings
from src.api.db.elastic import ApiElasticClient, get_api_elastic_client
from src.api.db.redis import ApiRedisClient, get_redis
from src.api.models.db.film import Film
from src.api.services.base import BaseElasticService


class FilmService(BaseElasticService):
    __key_prefix = "FilmService"
    __index = "movies"

    async def get_by_id(self, film_id: str) -> Film | None:
        key = self._redis.build_redis_key(self.__key_prefix, film_id)
        film = await self._redis.get_one_model(key, Film)
        if not film:
            film = await self.__get_film_from_elastic(film_id)
            if not film:
                return None
            await self._redis.set_one_model(key, film, self._cache_ex)
        return film

    async def get_films(
        self, page_number: int, page_size: int, genre_uuid: str, sort: str
    ) -> list[Film] | None:
        key = self._redis.build_redis_key(
            self.__key_prefix, page_number, page_size, genre_uuid, sort
        )
        films = await self._redis.get_list_model(key, Film)
        if not films:
            films = await self._get_films_from_elastic(
                page_number, page_size, genre_uuid, sort
            )
            if not films:
                return None
            await self._redis.set_list_model(key, films, self._cache_ex)
        return films

    async def get_search(
        self, page_number: int, page_size: int, query: str
    ) -> list[Film] | None:
        key = self._redis.build_redis_key(
            self.__key_prefix, page_number, page_size, query
        )
        films = await self._redis.get_list_model(key, Film)
        if not films:
            films = await self.__get_search_from_elastic(
                page_number, page_size, query
            )
            if not films:
                return None
            await self._redis.set_list_model(key, films, self._cache_ex)
        return films

    async def __get_film_from_elastic(self, film_id: str) -> Film | None:
        doc = await self._get_data_from_elastic(self.__index, film_id)
        if doc:
            return Film(**doc)
        return None

    async def _get_films_from_elastic(
        self, page_number: int, page_size: int, genre_uuid: str, sort_: str
    ) -> list[Film] | None:
        body = None
        sort = None
        if sort_:
            sort = []
            sort.append({sort_[1:]: "desc"}) if sort_[
                0
            ] == "-" else sort.append({sort_: "asc"})
        if genre_uuid:
            body = {
                "nested": {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": [{"match": {"genre.uuid": genre_uuid}}]
                        }
                    },
                }
            }

        try:
            docs = await self._elastic_client.get_async_client().search(
                index=self.__index,
                filter_path="hits.hits._source",
                query=body,
                from_=page_number,
                size=page_size,
                sort=sort,
            )
            if not docs:
                return None
        except (NotFoundError, ConnectionError):
            return None
        return [Film(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def __get_search_from_elastic(
        self,
        page_number: int,
        page_size: int,
        query: str,
    ) -> list[Film] | None:
        field = "title"
        docs = await self._get_search_from_elastic(
            self.__index, page_number, page_size, field, query
        )

        if docs:
            return [Film(**doc["_source"]) for doc in docs]
        return None


@lru_cache
def get_film_service(
    redis: ApiRedisClient = Depends(get_redis),
    elastic_client: ApiElasticClient = Depends(get_api_elastic_client),
) -> FilmService:
    return FilmService(redis, elastic_client, settings.cache_ex_for_films)
