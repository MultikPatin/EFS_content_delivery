from pydantic import BaseModel


class Genre(BaseModel):
    uuid: str
    name: str
    description: str | None
