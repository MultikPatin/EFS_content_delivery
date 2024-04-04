from logging import Logger
from typing import Any

from redis.asyncio import Redis

from src.api.cache.abstract import AbstractBaseModel, AbstractModelCache


class RedisCache(AbstractModelCache):
    """
    Клиент для работы api с Redis.

    Args:
        redis (Redis): объект для работы с Redis
        logger (Logger): объект для записи в журналы

    """

    __redis: Redis
    __logger: Logger

    def __init__(self, redis: Redis, logger: Logger):
        self.__redis = redis
        self.__logger = logger

    async def set_one_model(
        self,
        key: str,
        value: AbstractBaseModel,
        cache_expire: int,
    ) -> None:
        """
        Записать одну модель в кэш Redis.

        Args:
            key (str): ключ для записи модели
            value (AbstractBaseModel): модель для записи
            cache_expire (int): время жизни кэша в секундах

        """
        data = value.model_dump_json()
        try:
            await self.__redis.set(key, data, cache_expire)
        except Exception as set_error:
            self.__logger.error(
                "Error setting value with key `%s::%s`: %s.",
                key,
                value,
                set_error,
            )
            raise

    async def get_one_model(
        self, key: str, model: type[AbstractBaseModel]
    ) -> AbstractBaseModel | None:
        """
        Получить одну модель из кэша Redis.

        Args:
            key (str): ключ для получения модели
            model (AbstractBaseModel): модель для десериализации

        Returns:
            AbstractBaseModel | None: возвращает одну модель или None, если модель не найдена

        """
        try:
            value = await self.__redis.get(key)
            if not value:
                return None
        except Exception as get_error:
            self.__logger.error(
                "Error getting value with key `%s`: %s.", key, get_error
            )
            raise
        data = model.model_validate_json(value)
        return data

    async def set_list_model(
        self,
        key: str,
        values: list[AbstractBaseModel],
        cache_expire: int,
    ) -> None:
        """
        Записать список моделей в кэш Redis.

        Args:
            key (str): ключ для записи списка моделей
            values (list[AbstractBaseModel]): список моделей для записи
            cache_expire (int): время жизни кэша в секундах

        """
        try:
            for value in values:
                await self.__redis.lpush(key, value.model_dump_json())  # type: ignore
            await self.__redis.expire(key, cache_expire)
        except Exception as set_error:
            self.__logger.error(
                "Error setting values with key `%s::%s`: %s.",
                key,
                values,
                set_error,
            )
            raise

    async def get_list_model(
        self, key: str, model: type[AbstractBaseModel]
    ) -> list[AbstractBaseModel] | None:
        """
        Получить список моделей из кэша Redis.

        Args:
            key (str): ключ для получения списка моделей
            model (AbstractBaseModel): модель для десериализации

        Returns:
            list[AbstractBaseModel] | None: возвращает список моделей или None, если список не найден

        """
        try:
            list_count = await self.__redis.llen(key)  # type: ignore
            values = await self.__redis.lrange(key, 0, list_count)  # type: ignore
            values.reverse()
            if not values:
                return None
        except Exception as get_error:
            self.__logger.error(
                "Error getting values with key `%s`: %s.", key, get_error
            )
            raise
        data = []
        for value in values:
            data.append(model.model_validate_json(value))
        return data

    def build_key(self, key_prefix: str, *args: Any) -> str:
        """
        Создать ключ для кэша Redis.

        Args:
            key_prefix (str): префикс ключа
            *args: аргументы для создания ключа

        Returns:
            str: созданный ключ

        """
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

    async def close(self) -> None:
        """
        Закрыть соединение с Redis.

        """
        await self.__redis.aclose()
        self.__logger.info("Connection to Redis was closed.")

    async def ping(self) -> Any:
        """
        Ping the Redis server to ensure the connection is still alive.

        Returns:
            bool: True if the ping was successful, False if it failed.
        """
        return await self.__redis.ping()


redis: RedisCache | None = None


async def get_redis() -> RedisCache | None:
    return redis
