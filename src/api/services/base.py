from pydantic import BaseModel

from src.api.cache.abstract import AbstractModelCache
from src.api.db.abstract import AbstractDBClient


class BaseElasticService:
    _key_prefix: str
    _index: str

    def __init__(
        self,
        cache: AbstractModelCache,
        cache_ex: int,
        db: AbstractDBClient,
    ):
        self._cache = cache
        self._db = db
        self._cache_ex = cache_ex

    async def _get_by_id(
        self, obj_id: str, model: type[BaseModel]
    ) -> BaseModel | None:
        key = self._cache.build_key(self._key_prefix, obj_id)
        doc = await self._cache.get_one_model(key, model)
        if not doc:
            doc = await self._db.get_by_id(
                obj_id=obj_id, model=model, index=self._index
            )
            if not doc:
                return None
            await self._cache.set_one_model(key, doc, self._cache_ex)
        return doc

    async def _get_search(
        self,
        page_number: int,
        page_size: int,
        query: str | None,
        field: str,
        model: type[BaseModel],
    ) -> list[BaseModel] | None:
        key = self._cache.build_key(
            self._key_prefix, page_number, page_size, query
        )
        persons = await self._cache.get_list_model(key, model)
        if not persons:
            persons = await self._db.get_search_by_query(
                page_number=page_number,
                page_size=page_size,
                field=field,
                query=query,
                model=model,
                index=self._index,
            )
            if not persons:
                return None
            await self._cache.set_list_model(key, persons, self._cache_ex)
        return persons
