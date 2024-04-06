from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path

from src.api.core.utils import (
    build_films_field,
)
from src.api.models.api.v1.person import (
    FilmForFilms,
    Person,
)
from src.api.services.person import PersonService, get_person_service
from src.api.validators.pagination import PaginatedParams, get_paginated_params
from src.api.validators.search import search_query_validators

router = APIRouter()


@router.get(
    "/{person_id}", response_model=Person, summary="Get the details of a person"
)
async def person_details(
    person_uuid: Annotated[
        UUID,
        Path(
            alias="person_id",
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
    person = await person_service.get_by_id(person_uuid)
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
    page_number: int = 1,
    page_size: int = 50,
    search_query: Annotated[
        str | None,
        search_query_validators,
    ] = "",
    paginated_params: PaginatedParams = Depends(get_paginated_params),
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
    paginated_params.validate(page_number, page_size)
    persons = await person_service.get_search(
        **paginated_params.get(), search_query=search_query, field=field
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
    person_uuid: Annotated[
        UUID,
        Path(
            alias="person_id",
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
    films = await person_service.get_person_films(person_uuid)
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
