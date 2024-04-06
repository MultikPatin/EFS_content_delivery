from functools import lru_cache

from fastapi import Depends

from src.api.cache.redis import RedisCache, get_redis
from src.api.core.config import settings
from src.api.db.elastic import ElasticDB, get_elastic
from src.api.models.db.person import FilmForPersonDB, PersonDB
from src.api.services.base import BaseElasticService


class PersonService(BaseElasticService[PersonDB]):
    _key_prefix = "PersonService"
    _index = "persons"

    async def get_by_id(self, person_id: str) -> PersonDB | None:
        return await self._get_by_id(
            obj_id=person_id,
            model=PersonDB,
        )

    async def get_search(
        self,
        page_number: int,
        page_size: int,
        search_query: str | None,
        field: str,
    ) -> list[PersonDB] | None:
        return await self._get_search(
            page_number=page_number,
            page_size=page_size,
            search_query=search_query,
            field=field,
            model=PersonDB,
        )

    async def get_person_films(
        self,
        person_id: str,
    ) -> list[FilmForPersonDB] | None:
        key_prefix = self._key_prefix + "_films"
        key = self._cache.build_key(key_prefix, person_id)
        films = await self._cache.get_list_model(key, FilmForPersonDB)
        if not films:
            person = await self._db.get_by_id(
                obj_id=person_id, model=PersonDB, index=self._index
            )
            if not person:
                return None
            films = person.films
            if not films:
                return None
            await self._cache.set_list_model(key, films, self._cache_ex)
        return films


@lru_cache
def get_person_service(
    cache: RedisCache = Depends(get_redis),
    db: ElasticDB = Depends(get_elastic),
) -> PersonService:
    return PersonService(
        cache=cache,
        cache_ex=settings.cache_ex_for_films,
        db=db,
    )
