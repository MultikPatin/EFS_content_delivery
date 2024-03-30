from pydantic import BaseModel


class FilmMixin(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None

    class Meta:
        abstract = True


class FilmForPerson(FilmMixin):
    roles: list[str] | None


class Person(BaseModel):
    uuid: str
    full_name: str
    films: list[FilmForPerson] | None


class Film(FilmMixin): ...