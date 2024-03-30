from enum import Enum
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from src.api.models.api.v1.film import Film, FilmForFilmsList
from src.api.services.film import FilmService, get_film_service

router = APIRouter()


class ValidFieldsToSort(str, Enum):
    rating = "imdb_rating"
    desc_rating = "-imdb_rating"
    title = "title.raw"
    desc_title = "-title.raw"


@router.get("/{film_id}", response_model=Film, summary="Get film details by id")
async def film_details(
    film_id: Annotated[
        str,
        Path(
            title="film id",
            description="The UUID of the film to get like: 8f128d84-dd99-4d0d-a9c8-df11f87ac133",
        ),
    ],
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    """
    Get film details by id

    Args:
    - **film_id** (str): The UUID of the film to get

    Returns:
    - **Film**: The film with the given ID

    Raises:
        HTTPException: If the film does not exist
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found"
        )

    return Film(
        uuid=film.uuid,
        title=film.title,
        imdb_rating=film.imdb_rating,
        genre=film.genre,
        description=film.description,
        directors=film.directors,
        actors=film.actors,
        writers=film.writers,
    )


@router.get(
    "/", response_model=list[FilmForFilmsList], summary="Get a list of films"
)
async def films(
    page_number: Annotated[
        int,
        Query(
            title="Page number",
            description="The number of the page to get",
            ge=1,
            le=10000,
        ),
    ] = 1,
    page_size: Annotated[
        int,
        Query(
            title="Page size",
            description="The size of the page to get",
            ge=1,
            le=10000,
        ),
    ] = 50,
    genre: Annotated[
        str | None,
        Query(
            title="Genre UUID",
            description="The UUID of the genre to filter movies",
            example="6a0a479b-cfec-41ac-b520-41b2b007b611",
        ),
    ] = None,
    sort: Annotated[
        ValidFieldsToSort,
        Query(
            title="Sort field",
            description="The name of the field to sort movies like: imdb_rating (for descending sort needs '-' before sort: -imdb_rating)",
            examples=["title.raw", "imdb_rating"],
        ),
    ] = None,
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmForFilmsList]:
    """
    Get a list of films.

    Args:
    - **page_number** (int): The number of the page to get (default: 1)
    - **page_size** (int): The size of the page to get (default: 5)
    - **genre** (str): The UUID of the genre to filter movies
    - **sort** (ValidFieldsToSort): The name of the field to sort movies

    Returns:
    - **list[FilmForFilmsList]**: The list of films

    Raises:
        HTTPException: If no films are found
    """
    films = await film_service.get_films(page_number, page_size, genre, sort)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found"
        )
    return [
        FilmForFilmsList(
            uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]


@router.get(
    "/search/",
    response_model=list[FilmForFilmsList],
    summary="Get a list of films based on a search query",
)
async def films_search(
    page_number: Annotated[
        int,
        Query(
            title="Page number",
            description="The number of the page to get",
            ge=1,
            le=10000,
        ),
    ] = 1,
    page_size: Annotated[
        int,
        Query(
            title="Page size",
            description="The size of the page to get",
            ge=1,
            le=10000,
        ),
    ] = 50,
    query: Annotated[
        str | None,
        Query(
            title="Search query",
            description="The query to search movies",
        ),
    ] = "",
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmForFilmsList]:
    """
    Get a list of films based on a search query.

    Args:
    - **page_number** (int): The number of the page to get (default: 1)
    - **page_size** (int): The size of the page to get (default: 5)
    - **query** (str): The query to search movies

    Returns:
    - **list[FilmForFilmsList]**: The list of films

    Raises:
        HTTPException: If no films are found
    """
    films = await film_service.get_search(page_number, page_size, query)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found"
        )
    return [
        FilmForFilmsList(
            uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]
