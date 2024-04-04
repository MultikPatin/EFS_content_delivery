from src.api.models.base import FilmMixin, UUIDMixin


class FilmForPerson(UUIDMixin):
    roles: list[str] | None


class Person(UUIDMixin):
    full_name: str
    films: list[FilmForPerson] | None


class FilmForFilms(FilmMixin):
    pass
