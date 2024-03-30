from functools import lru_cache

from fastapi import Depends

from src.api.cache.redis import RedisCache, get_redis
from src.api.core.config import settings
from src.api.db.elastic import ElasticDB, get_elastic
from src.api.models.db.film import Film
from src.api.services.base import BaseElasticService


class FilmService(BaseElasticService):
    __key_prefix = "FilmService"
    __index = "movies"

    async def get_by_id(self, film_id: str) -> Film | None:
        key = self._cache.build_key(self.__key_prefix, film_id)
        film = await self._cache.get_one_model(key, Film)
        if not film:
            film = await self._db.get_by_id(obj_id=film_id, index=self.__index)
            if not film:
                return None
            film = Film(**film)
            await self._cache.set_one_model(key, film, self._cache_ex)
        return film

    async def get_films(
        self, page_number: int, page_size: int, genre_uuid: str, sort: str
    ) -> list[Film] | None:
        key = self._cache.build_key(
            self.__key_prefix, page_number, page_size, genre_uuid, sort
        )
        films = await self._cache.get_list_model(key, Film)
        if not films:
            films = await self.__get_films_from_elastic(
                page_number, page_size, genre_uuid, sort
            )
            if not films:
                return None
            films = [Film(**film["_source"]) for film in films]
            await self._cache.set_list_model(key, films, self._cache_ex)
        return films

    async def get_search(
        self, page_number: int, page_size: int, query: str
    ) -> list[Film] | None:
        field = "title"
        key = self._cache.build_key(
            self.__key_prefix, page_number, page_size, query
        )
        films = await self._cache.get_list_model(key, Film)
        if not films:
            films = await self._db.get_search_by_query(
                page_number=page_number,
                page_size=page_size,
                field=field,
                query=query,
                index=self.__index,
            )
            if not films:
                return None
            films = [Film(**film["_source"]) for film in films]
            await self._cache.set_list_model(key, films, self._cache_ex)
        return films

    async def __get_films_from_elastic(
        self, page_number: int, page_size: int, genre_uuid: str, sort_: str
    ) -> list[dict] | None:
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
            index=self.__index,
            filter_path="hits.hits._source",
            query=query,
            page_number=page_number,
            page_size=page_size,
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
