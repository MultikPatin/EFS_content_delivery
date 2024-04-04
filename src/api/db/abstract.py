from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

AbstractBaseModel = TypeVar("AbstractBaseModel", bound=BaseModel)


class AbstractDBClient(ABC):
    """
    Abstract class for interacting with a database.
    """

    @abstractmethod
    async def get_by_id(
        self, obj_id: str, model: type[AbstractBaseModel], **kwargs: Any
    ) -> AbstractBaseModel | None:
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The ID of the object to retrieve.
            model (AbstractBaseModel): The model to get.
            **kwargs: Additional arguments to pass to the database.

        Returns:
            AbstractBaseModel | None: The object with the given ID, or None if no object was found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        page_number: int,
        page_size: int,
        model: type[AbstractBaseModel],
        **kwargs: Any,
    ) -> list[AbstractBaseModel] | None:
        """
        Retrieve a list of all objects.

        Args:
            page_number (int): The page number to retrieve.
            page_size (int): The number of objects to retrieve per page.
            model (AbstractBaseModel): The model to get.
            **kwargs: Additional arguments to pass to the database.

        Returns:
            list[AbstractBaseModel] | None: A list of objects, or None if no objects were found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_search_by_query(
        self,
        page_number: int,
        page_size: int,
        field: str,
        query: str | None,
        model: type[AbstractBaseModel],
        **kwargs: Any,
    ) -> list[AbstractBaseModel] | None:
        """
        Retrieve a list of objects that match a search query.

        Args:
            page_number (int): The page number to retrieve.
            page_size (int): The number of objects to retrieve per page.
            field (str): The field to search by.
            query (str): The search query.
            model (AbstractBaseModel): The model to get.
            **kwargs: Additional arguments to pass to the database.

        Returns:
            list[AbstractBaseModel] | None: A list of objects that match the search query, or None if no objects were found.
        """
        raise NotImplementedError
