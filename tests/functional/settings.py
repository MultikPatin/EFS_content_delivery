import os
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv.main import find_dotenv, load_dotenv
from tests.functional.testdata.es_mapping import _ELASTIC_SETTINGS, _FILMS_ELASTIC_MAPPING, _GENRES_ELASTIC_MAPPING, _PERSONS_ELASTIC_MAPPING


load_dotenv(find_dotenv(".env"))

class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    es_host: str = "http://127.0.0.1:9200"
    es_port: int = Field(..., alias="ELASTIC_PORT")
    es_movies_index: str = "movies"
    es_id_field: str = "uuid"
    es_index_mapping: dict = {'films_mapping':_FILMS_ELASTIC_MAPPING, 'genres_mapping': _GENRES_ELASTIC_MAPPING, 'persons_mapping': _PERSONS_ELASTIC_MAPPING}
    es_index_settings: dict = _ELASTIC_SETTINGS


    redis_host: str = ""
    service_url: str = "http://127.0.0.1"

    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_settings = TestSettings()
