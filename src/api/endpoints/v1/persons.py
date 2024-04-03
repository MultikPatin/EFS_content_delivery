from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path

from src.api.core.utils import (
    build_films_field,
    page_number_query,
    page_size_query,
    search_query,
)
from src.api.models.api.v1.person import (
    FilmForFilms,
    Person,
)
from src.api.services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/{person_id}", response_model=Person, summary="Get the details of a person"
)
async def person_details(
    person_id: Annotated[
        UUID,
        Path(
            title="person id",
            description="The UUID of the person to get",
            example="b445a536-338c-4e7a-a79d-8f9c2e41ca85",
        ),
    ],
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    """Get the details of a person.

    Args:
    - **person_id** (str): The UUID of the person to get.

    Returns:
    - **Person**: The person details.

    Raises:
        HTTPException: If the person is not found.
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found"
        )
    return Person(
        uuid=person.uuid,
        full_name=person.full_name,
        films=build_films_field(person),
    )


@router.get(
    "/search/",
    response_model=list[Person],
    summary="Get a list of persons based on a search query",
)
async def persons_search_by_full_name(
    page_number: Annotated[
        int,
        page_number_query,
    ] = 1,
    page_size: Annotated[
        int,
        page_size_query,
    ] = 50,
    query: Annotated[
        str | None,
        search_query,
    ] = "",
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    """Get a list of persons based on a search query

    Args:
    - **page_number** (int, optional): The number of the page to get. Defaults to 1.
    - **page_size** (int, optional): The size of the page to get. Defaults to 5.
    - **query** (str, optional): The query to search persons. Defaults to None.

    Returns:
    - **list[Person]**: A list of persons.

    Raises:
        HTTPException: If the persons are not found.
    """
    field = "full_name"
    persons = await person_service.get_search(
        page_number, page_size, query, field
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    return [
        Person(
            uuid=person.uuid,
            full_name=person.full_name,
            films=build_films_field(person),
        )
        for person in persons
    ]


@router.get(
    "/{person_id}/film/",
    response_model=list[FilmForFilms],
    summary="Get a list of films for a specific person",
)
async def person_details_films(
    person_id: Annotated[
        UUID,
        Path(
            title="person id",
            description="The UUID of the person to get",
            example="b445a536-338c-4e7a-a79d-8f9c2e41ca85",
        ),
    ],
    person_service: PersonService = Depends(get_person_service),
) -> list[FilmForFilms]:
    """Get a list of films for a specific person

    Args:
    - **person_id** (str): The UUID of the person to get

    Returns:
    - **list[FilmForFilms]**: A list of films for a specific person

    Raises:
        HTTPException: If the films are not found.
    """
    films = await person_service.get_person_films(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="films not found"
        )
    return [
        FilmForFilms(
            uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]
