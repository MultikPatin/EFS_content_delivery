from typing import Any

from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv.main import find_dotenv, load_dotenv
from tests.functional.testdata.es_mapping import (
    ELASTIC_SETTINGS,
    FILMS_ELASTIC_MAPPING,
    GENRES_ELASTIC_MAPPING,
    PERSONS_ELASTIC_MAPPING,
)

load_dotenv(find_dotenv(".env"))


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    local: str = Field("True", alias="LOCAL")
    es_host: str = Field(..., alias="ELASTIC_HOST")
    es_port: int = Field(9200, alias="ELASTIC_PORT")
    es_id_field: str = "uuid"
    es_index_data: dict[str, dict[str, Any]] = {
        "films": {
            "name": "test_movies",
            "mappings": FILMS_ELASTIC_MAPPING,
            "settings": ELASTIC_SETTINGS,
        },
        "genres": {
            "name": "test_genres",
            "mappings": GENRES_ELASTIC_MAPPING,
            "settings": ELASTIC_SETTINGS,
        },
        "persons": {
            "name": "test_persons",
            "mappings": PERSONS_ELASTIC_MAPPING,
            "settings": ELASTIC_SETTINGS,
        },
    }
    redis_host: str = Field(default=..., alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    @property
    def get_es_host(self) -> str:
        if self.local == "True":
            return f"http://127.0.0.1:{self.es_port}"
        return f"http://{self.es_host}:{self.es_port}"

    @property
    def get_redis_host(self) -> dict[str, Any]:
        if self.local == "True":
            return {"host": "127.0.0.1", "port": self.es_port}
        return {"host": self.es_host, "port": self.es_port}


settings = TestSettings()
