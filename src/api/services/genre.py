from functools import lru_cache

from elastic_transport import ConnectionError
from elasticsearch import NotFoundError
from fastapi import Depends

from src.api.core.config import settings
from src.api.db.cache.redis import RedisCache, get_redis
from src.api.db.elastic import ApiElasticClient, get_api_elastic_client
from src.api.models.db.genre import Genre
from src.api.services.base import BaseElasticService


class GenreService(BaseElasticService):
    __key_prefix = "GenreService"
    __index = "genres"

    async def get_by_id(self, genre_id: str) -> Genre | None:
        key = self._cache.build_key(self.__key_prefix, genre_id)
        genre = await self._cache.get_one_model(key, Genre)
        if not genre:
            genre = await self.__get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._cache.set_one_model(key, genre, self._cache_ex)
        return genre

    async def get_genres(
        self, page_number: int, page_size: int
    ) -> list[Genre] | None:
        key = self._cache.build_key(self.__key_prefix, page_number, page_size)
        genres = await self._cache.get_list_model(key, Genre)
        if not genres:
            genres = await self.__get_genres_from_elastic(
                page_number, page_size
            )
            if not genres:
                return None
            await self._cache.set_list_model(key, genres, self._cache_ex)
        return genres

    async def __get_genre_from_elastic(self, genre_id: str) -> Genre | None:
        doc = await self._get_data_from_elastic(self.__index, genre_id)
        if doc:
            return Genre(**doc)
        return None

    async def __get_genres_from_elastic(
        self,
        page_number: int,
        page_size: int,
    ) -> list[Genre] | None:
        try:
            docs = await self._elastic_client.get_async_client().search(
                index=self.__index,
                from_=page_number,
                size=page_size,
            )
        except (NotFoundError, ConnectionError):
            return None
        return [Genre(**doc["_source"]) for doc in docs["hits"]["hits"]]


@lru_cache
def get_genre_service(
    cache: RedisCache = Depends(get_redis),
    elastic_client: ApiElasticClient = Depends(get_api_elastic_client),
) -> GenreService:
    return GenreService(
        cache=cache,
        cache_ex=settings.cache_ex_for_films,
        elastic_client=elastic_client,
    )
