import os
from logging import config as logging_config

from dotenv.main import find_dotenv, load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.api.core.logger import LOGGING
from src.core.configs.elastic import ElasticSettings
from src.core.configs.redis import RedisSettings

load_dotenv(find_dotenv(".env"))

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    elastic: ElasticSettings = ElasticSettings()
    redis: RedisSettings = RedisSettings()
    name: str = Field(..., alias="API_PROJECT_NAME")
    description: str = Field(..., alias="API_PROJECT_DESCRIPTION")
    docs_url: str = Field(..., alias="API_DOCS_URL")
    openapi_url: str = Field(..., alias="API_OPENAPI_URL")
    host: str = Field(..., alias="API_HOST")
    port: int = Field(..., alias="API_PORT")

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    cache_ex_for_films: int = Field(
        ..., alias="API_CACHE_EXPIRE_FOR_FILM_SERVICE"
    )
    cache_ex_for_genres: int = Field(
        ..., alias="API_CACHE_EXPIRE_FOR_GENRES_SERVICE"
    )
    cache_ex_for_persons: int = Field(
        ..., alias="API_CACHE_EXPIRE_FOR_PERSON_SERVICE"
    )


settings = Settings()
