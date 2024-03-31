from pydantic import BaseModel

from src.api.cache import AbstractModelCache
from src.api.db import AbstractDBClient


class BaseElasticService:
    _base_model: BaseModel = BaseModel()

    def __init__(
        self,
        cache: AbstractModelCache,
        cache_ex: int,
        db: AbstractDBClient,
    ):
        self._cache = cache
        self._db = db
        self._cache_ex = cache_ex
