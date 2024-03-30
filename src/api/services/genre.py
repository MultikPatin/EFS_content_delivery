from functools import lru_cache

from fastapi import Depends

from src.api.cache.redis import RedisCache, get_redis
from src.api.core.config import settings
from src.api.db.elastic import ElasticDB, get_elastic
from src.api.models.db.genre import Genre
from src.api.services.base import BaseElasticService


class GenreService(BaseElasticService):
    __key_prefix = "GenreService"
    __index = "genres"

    async def get_by_id(self, genre_id: str) -> Genre | None:
        key = self._cache.build_key(self.__key_prefix, genre_id)
        genre = await self._cache.get_one_model(key, Genre)
        if not genre:
            genre = await self._db.get_by_id(
                obj_id=genre_id, index=self.__index
            )
            if not genre:
                return None
            genre = Genre(**genre)
            await self._cache.set_one_model(key, genre, self._cache_ex)
        return genre

    async def get_genres(
        self, page_number: int, page_size: int
    ) -> list[Genre] | None:
        key = self._cache.build_key(self.__key_prefix, page_number, page_size)
        genres = await self._cache.get_list_model(key, Genre)
        if not genres:
            genres = await self._db.get_all(
                page_number=page_number, page_size=page_size, index=self.__index
            )
            if not genres:
                return None
            genres = [Genre(**genre["_source"]) for genre in genres]
            await self._cache.set_list_model(key, genres, self._cache_ex)
        return genres


@lru_cache
def get_genre_service(
    cache: RedisCache = Depends(get_redis),
    db: ElasticDB = Depends(get_elastic),
) -> GenreService:
    return GenreService(
        cache=cache,
        cache_ex=settings.cache_ex_for_films,
        db=db,
    )
