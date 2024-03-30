from functools import lru_cache

from fastapi import Depends

from src.api.core.config import settings
from src.api.db.elastic import ApiElasticClient, get_api_elastic_client
from src.api.db.redis import ApiRedisClient, get_redis
from src.api.models.db.person import (
    Film,
    Person,
)
from src.api.services.base import BaseElasticService


class PersonService(BaseElasticService):
    __key_prefix = "PersonService"
    __index = "persons"

    async def get_by_id(self, person_id: str) -> Person | None:
        key = self._redis.build_redis_key(self.__key_prefix, person_id)
        person = await self._redis.get_one_model(key, Person)
        if not person:
            person = await self.__get_person_from_elastic(person_id)
            if not person:
                return None
            await self._redis.set_one_model(key, person, self._cache_ex)
        return person

    async def get_search(
        self, page_number: int, page_size: int, query: str
    ) -> list[Person] | None:
        key = self._redis.build_redis_key(
            self.__key_prefix, page_number, page_size, query
        )
        persons = await self._redis.get_list_model(key, Person)
        if not persons:
            persons = await self.__get_search_from_elastic(
                page_number, page_size, query
            )
            if not persons:
                return None
            await self._redis.set_list_model(key, persons, self._cache_ex)
        return persons

    async def get_person_films(
        self,
        person_id: str,
    ) -> list[Film] | None:
        self.__key_prefix += "_films"
        key = self._redis.build_redis_key(
            self.__key_prefix,
            person_id,
        )
        films = await self._redis.get_list_model(key, Film)
        if not films:
            films = await self.__get_person_films_from_elastic(person_id)
            if not films:
                return None
            await self._redis.set_list_model(key, films, self._cache_ex)
        return films

    async def __get_person_from_elastic(self, person_id: str) -> Person | None:
        doc = await self._get_data_from_elastic(self.__index, person_id)
        if doc:
            return Person(**doc)
        return None

    async def __get_search_from_elastic(
        self,
        page_number: int,
        page_size: int,
        query: str,
    ) -> list[Person] | None:
        field = "full_name"
        docs = await self._get_search_from_elastic(
            self.__index, page_number, page_size, field, query
        )

        if docs:
            return [Person(**doc["_source"]) for doc in docs]
        return None

    async def __get_person_films_from_elastic(
        self, person_id: str
    ) -> list[Film] | None:
        docs = await self._get_data_from_elastic(self.__index, person_id)
        if not docs:
            return None

        return [Film(**film) for film in docs["films"]]


@lru_cache
def get_person_service(
    redis: ApiRedisClient = Depends(get_redis),
    elastic_client: ApiElasticClient = Depends(get_api_elastic_client),
) -> PersonService:
    return PersonService(redis, elastic_client, settings.cache_ex_for_persons)
