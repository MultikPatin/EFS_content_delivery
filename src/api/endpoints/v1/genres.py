from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path

from src.api.models.api.v1.genre import Genre
from src.api.services.genre import GenreService, get_genre_service
from src.api.validators.pagination import PaginatedParams, get_paginated_params

router = APIRouter()


@router.get(
    "/{genre_id}", response_model=Genre, summary="Get genre details by id"
)
async def genre_details(
    genre_uuid: Annotated[
        UUID,
        Path(
            alias="genre_id",
            title="genre id",
            description="The UUID of the genre to get",
            example="6a0a479b-cfec-41ac-b520-41b2b007b611",
        ),
    ],
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    """Get genre details by id

    Args:
    - **genre_id** (str): The UUID of the genre to get

    Returns:
    - **Genre**: The genre with the given id

    Raises:
        HTTPException: If the genre is not found
    """
    genre = await genre_service.get_by_id(genre_uuid)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genre not found"
        )
    return Genre(uuid=genre.uuid, name=genre.name)


@router.get("/", response_model=list[Genre], summary="Get a list of genres")
async def genres(
    page_number: int = 1,
    page_size: int = 50,
    paginated_params: PaginatedParams = Depends(get_paginated_params),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    """Get a list of genres

    Args:
    - **page_number** (int, optional): The number of the page to get (default: 1)
    - **page_size** (int, optional): The size of the page to get (default: 5)

    Returns:
    - **list[Genre]**: The list of genres

    Raises:
        HTTPException: If the genres are not found
    """
    paginated_params.validate(page_number, page_size)
    genres = await genre_service.get_genres(**paginated_params.get())
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genres not found"
        )
    return [Genre(uuid=genre.uuid, name=genre.name) for genre in genres]
