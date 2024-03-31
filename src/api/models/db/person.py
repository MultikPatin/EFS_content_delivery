from src.api.models.base import FilmMixin, UUIDMixin


class FilmForPersonDB(FilmMixin):
    roles: list[str] | None


class PersonDB(UUIDMixin):
    full_name: str
    films: list[FilmForPersonDB] | None
