from fastapi import HTTPException


class PaginatedParams:
    __page_number: int
    __page_size: int

    def validate(self, page_number: int, page_size: int):
        self.__page_number = page_number
        self.__page_size = page_size
        self.__validate_page_number()
        self.__validate_page_size()

    def __validate_page_number(self):
        if self.__page_number < 1 or self.__page_number > 100:
            raise HTTPException(
                status_code=422,
                detail="Page number must be greater than 0 and less than 100",
            )

    def __validate_page_size(self):
        if self.__page_size < 1 or self.__page_size > 100:
            raise HTTPException(
                status_code=422,
                detail="Page size must be greater than 0 and less than 100",
            )

    def get(self):
        return {
            "page_number": self.__page_number,
            "page_size": self.__page_size,
        }


def get_paginated_params() -> PaginatedParams:
    return PaginatedParams()
