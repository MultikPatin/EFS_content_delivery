from enum import Enum

from fastapi import Query

from src.api.models.api.v1.person import FilmForPerson
from src.api.models.db.person import PersonDB


def build_films_field(person: PersonDB) -> list[FilmForPerson] | None:
    if person.films:
        return [
            FilmForPerson(uuid=film.uuid, roles=film.roles)
            for film in person.films
        ]
    else:
        return None


page_number_query = Query(
    title="Page number",
    description="The number of the page to get",
    ge=1,
    le=100,
)

page_size_query = Query(
    title="Page size",
    description="The size of the page to get",
    ge=1,
    le=100,
)

search_query = Query(
    title="Search query",
    description="The query to search",
)


class FilmFieldsToSort(str, Enum):
    rating = "imdb_rating"
    desc_rating = "-imdb_rating"
    asc_title = "title.raw"
    desc_title = "-title.raw"
