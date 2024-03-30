from pydantic import BaseModel


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float | None
    description: str | None
    genre: list | None
    directors: list | None
    actors: list | None
    writers: list | None
