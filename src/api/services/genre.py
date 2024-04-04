from functools import lru_cache

from fastapi import Depends

from src.api.cache.redis import RedisCache, get_redis
from src.api.core.config import settings
from src.api.db.elastic import ElasticDB, get_elastic
from src.api.models.db.genre import GenreDB
from src.api.services.base import BaseElasticService


class GenreService(BaseElasticService[GenreDB]):
    _key_prefix = "GenreService"
    _index = "genres"

    async def get_by_id(self, genre_id: str) -> GenreDB | None:
        return await self._get_by_id(
            obj_id=genre_id,
            model=GenreDB,
        )

    async def get_genres(
        self, page_number: int, page_size: int
    ) -> list[GenreDB] | None:
        key = self._cache.build_key(self._key_prefix, page_number, page_size)
        genres = await self._cache.get_list_model(key, GenreDB)
        if not genres:
            genres = await self._db.get_all(
                page_number=page_number,
                page_size=page_size,
                model=GenreDB,
                index=self._index,
            )
            if not genres:
                return None
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
