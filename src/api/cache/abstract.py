from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

AbstractBaseModel = TypeVar("AbstractBaseModel", bound=BaseModel)


class AbstractModelCache(ABC):
    """
    Abstract base class for caching.

    Provides an interface for caching objects of type ModelType.
    """

    @abstractmethod
    async def set_one_model(
        self,
        key: str,
        value: AbstractBaseModel,
        cache_expire: int,
    ) -> None:
        """
        Set a single model in the cache.

        Args:
            key (str): The key to use for caching the model.
            value (AbstractBaseModel): The model to cache.
            cache_expire (int): The number of seconds until the model expires.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_one_model(
        self, key: str, model: type[AbstractBaseModel]
    ) -> AbstractBaseModel | None:
        """
        Get a single model from the cache.

        Args:
            key (str): The key used for caching the model.
            model (AbstractBaseModel): The model class to cast the cached value to.

        Returns:
            The cached model, or None if the model is not in the cache.
        """
        raise NotImplementedError

    @abstractmethod
    async def set_list_model(
        self,
        key: str,
        values: list[AbstractBaseModel],
        cache_expire: int,
    ) -> None:
        """
        Set a list of models in the cache.

        Args:
            key (str): The key to use for caching the list of models.
            values (list[AbstractBaseModel]): The list of models to cache.
            cache_expire (int): The number of seconds until the list of models expires.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_list_model(
        self, key: str, model: type[AbstractBaseModel]
    ) -> list[AbstractBaseModel] | None:
        """
        Get a list of models from the cache.

        Args:
            key (str): The key used for caching the list of models.
            model (AbstractBaseModel): The model class to cast the cached values to.

        Returns:
            The cached list of models, or None if the list of models is not in the cache.
        """
        raise NotImplementedError

    @abstractmethod
    def build_key(self, key_prefix: str, *args: Any) -> str:
        """
        Build a cache key.

        Args:
            key_prefix (str): The prefix to use for the cache key.
            *args: Additional arguments to include in the cache key.

        Returns:
            The built cache key.
        """
        raise NotImplementedError
