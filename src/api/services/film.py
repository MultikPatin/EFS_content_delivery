from functools import lru_cache

from fastapi import Depends

from src.api.cache.redis import RedisCache, get_redis
from src.api.core.config import settings
from src.api.db.elastic import ElasticDB, get_elastic
from src.api.models.db.film import FilmDB
from src.api.services.base import BaseElasticService


class FilmService(BaseElasticService[FilmDB]):
    _key_prefix = "FilmService"
    _index = "movies"

    async def get_by_id(self, film_id: str) -> FilmDB | None:
        return await self._get_by_id(
            obj_id=film_id,
            model=FilmDB,
        )

    async def get_films(
        self,
        page_number: int,
        page_size: int,
        genre_uuid: str | None,
        sort: str | None,
    ) -> list[FilmDB] | None:
        key = self._cache.build_key(
            self._key_prefix, page_number, page_size, genre_uuid, sort
        )
        films = await self._cache.get_list_model(key, FilmDB)
        if not films:
            films = await self.__get_films_from_elastic(
                page_number, page_size, genre_uuid, sort
            )
            if not films:
                return None
            await self._cache.set_list_model(key, films, self._cache_ex)
        return films

    async def get_search(
        self,
        page_number: int,
        page_size: int,
        search_query: str | None,
        field: str,
    ) -> list[FilmDB] | None:
        return await self._get_search(
            page_number=page_number,
            page_size=page_size,
            search_query=search_query,
            field=field,
            model=FilmDB,
        )

    async def __get_films_from_elastic(
        self,
        page_number: int,
        page_size: int,
        genre_uuid: str | None,
        sort_: str | None,
    ) -> list[FilmDB] | None:
        query = None
        sort = None
        if sort_:
            sort = []
            sort.append({sort_[1:]: "desc"}) if sort_[
                0
            ] == "-" else sort.append({sort_: "asc"})
        if genre_uuid:
            query = {
                "nested": {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": [{"match": {"genre.uuid": genre_uuid}}]
                        }
                    },
                }
            }

        return await self._db.get_all(
            page_number=page_number,
            page_size=page_size,
            model=FilmDB,
            index=self._index,
            filter_path="hits.hits._source",
            query=query,
            sort=sort,
        )


@lru_cache
def get_film_service(
    cache: RedisCache = Depends(get_redis),
    db: ElasticDB = Depends(get_elastic),
) -> FilmService:
    return FilmService(
        cache=cache,
        cache_ex=settings.cache_ex_for_films,
        db=db,
    )
