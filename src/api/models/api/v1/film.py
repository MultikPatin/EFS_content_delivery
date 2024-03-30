from pydantic import BaseModel


class FilmMixin(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None

    class Meta:
        abstract = True


class Film(FilmMixin):
    description: str | None
    genre: list | None
    directors: list | None
    actors: list | None
    writers: list | None


class FilmForFilmsList(FilmMixin): ...
