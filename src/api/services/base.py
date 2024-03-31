from src.api.cache.abstract import AbstractModelCache
from src.api.db.abstract import AbstractDBClient


class BaseElasticService:
    def __init__(
        self,
        cache: AbstractModelCache,
        cache_ex: int,
        db: AbstractDBClient,
    ):
        self._cache = cache
        self._db = db
        self._cache_ex = cache_ex
