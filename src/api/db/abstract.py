from abc import ABC, abstractmethod


class AbstractDBClient(ABC):
    """
    Abstract class for interacting with a database.
    """

    @abstractmethod
    async def get_by_id(self, obj_id: str, **kwargs) -> dict | None:
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The ID of the object to retrieve.

        Returns:
            dict | None: The object with the given ID, or None if no object was found.
        """
        pass

    @abstractmethod
    async def get_all(
        self, page_number: int, page_size: int, **kwargs
    ) -> list[dict] | None:
        """
        Retrieve a list of all objects.

        Args:
            page_number (int): The page number to retrieve.
            page_size (int): The number of objects to retrieve per page.
            *args: Additional arguments to pass to the database.

        Returns:
            list[dict] | None: A list of objects, or None if no objects were found.
        """
        pass

    @abstractmethod
    async def get_search_by_query(
        self, page_number: int, page_size: int, field: str, query: str, **kwargs
    ) -> list[dict] | None:
        """
        Retrieve a list of objects that match a search query.

        Args:
            page_number (int): The page number to retrieve.
            page_size (int): The number of objects to retrieve per page.
            field (str): The field to search by.
            query (str): The search query.

        Returns:
            list[dict] | None: A list of objects that match the search query, or None if no objects were found.
        """
        pass
