from logging import Logger

from pydantic import BaseModel
from redis.asyncio import Redis


class ApiRedisClient:
    """Клиент для работы api с Redis."""

    __redis: Redis
    __logger: Logger

    def __init__(self, redis: Redis, logger: Logger):
        self.__redis = redis
        self.__logger = logger

    async def set_one_model(
        self,
        key: str,
        value: BaseModel,
        cache_expire: int,
    ) -> None:
        data = value.model_dump_json()
        try:
            await self.__redis.set(key, data, cache_expire)
        except Exception as set_error:
            self.__logger.error(
                f"Error setting values with key `{key}::{value}`: {set_error}."
            )
            raise

    async def get_one_model(self, key: str, model) -> BaseModel | None:
        try:
            value = await self.__redis.get(key)
            if not value:
                return None
        except Exception as get_error:
            self.__logger.error(
                f"Error getting value with key `{key}`: `{get_error}."
            )
            raise
        data = model.model_validate_json(value)
        return data

    async def set_list_model(
        self,
        key: str,
        values: list[BaseModel],
        cache_expire: int,
    ) -> None:
        try:
            for value in values:
                await self.__redis.lpush(key, value.model_dump_json())
            await self.__redis.expire(key, cache_expire)
        except Exception as set_error:
            self.__logger.error(
                f"Error setting values with key `{key}::{values}`: {set_error}."
            )
            raise

    async def get_list_model(self, key: str, model) -> list[BaseModel] | None:
        try:
            list_count = await self.__redis.llen(key)
            end = 0 - list_count
            values = await self.__redis.lrange(key, -1, end)
            if not values:
                return None
        except Exception as get_error:
            self.__logger.error(
                f"Error getting value with key `{key}`: `{get_error}."
            )
            raise
        data = []
        for value in values:
            data.append(model.model_validate_json(value))
        return data

    def build_redis_key(self, key_prefix: str, *args) -> str:
        if not key_prefix:
            self.__logger.error("Key prefix value is required")
            raise
        key = ""
        for arg in args:
            key += f"{str(arg)}:"
        if not key:
            self.__logger.error("key value is required")
            raise
        return f"{key_prefix}-{key}"

    async def close(self):
        await self.__redis.aclose()
        self.__logger.info("Connection to Redis was closed.")


api_redis_client: ApiRedisClient | None = None


async def get_redis() -> ApiRedisClient:
    return api_redis_client
