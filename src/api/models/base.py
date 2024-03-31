from pydantic import BaseModel


class UUIDMixin(BaseModel):
    uuid: str

    class Meta:
        abstract = True


class FilmMixin(UUIDMixin):
    title: str
    imdb_rating: float | None

    class Meta:
        abstract = True


class FilmFullMixin(FilmMixin):
    description: str | None
    genre: list[dict[str, str]] | None
    directors: list[dict[str, str]] | None
    actors: list[dict[str, str]] | None
    writers: list[dict[str, str]] | None

    class Meta:
        abstract = True
