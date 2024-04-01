import os
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv.main import find_dotenv, load_dotenv

from src.core.configs.elastic import ElasticSettings
# from src.core.configs.redis import RedisSettings

load_dotenv(find_dotenv(".env"))

_ELASTIC_SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {"type": "stop", "stopwords": "_english_"},
            "english_stemmer": {
                "type": "stemmer",
                "language": "english",
            },
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english",
            },
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {
                "type": "stemmer",
                "language": "russian",
            },
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer",
                ],
            }
        },
    },
}

_ELASTIC_MAPPING = {
    "dynamic": "strict",
    "properties": {
        "uuid": {"type": "keyword"},
        "imdb_rating": {"type": "float"},
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {"raw": {"type": "keyword"}},
        },
        "description": {"type": "text", "analyzer": "ru_en"},
        "genre": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "uuid": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "directors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "uuid": {"type": "keyword"},
                "full_name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "uuid": {"type": "keyword"},
                "full_name": {"type": "text", "analyzer": "ru_en"},
            },
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "uuid": {"type": "keyword"},
                "full_name": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    es_host: str = "http://127.0.0.1:9200"
    # es_host: str = Field(..., alias="ELASTIC_HOST")
    es_port: int = Field(..., alias="ELASTIC_PORT")
    es_index: str = "movies"
    es_id_field: str = ""
    es_index_mapping: dict = _ELASTIC_MAPPING
    es_index_settings: dict = _ELASTIC_SETTINGS

    # elastic: ElasticSettings = ElasticSettings()
    # redis: RedisSettings = RedisSettings()

    redis_host: str = ""
    service_url: str = "http://127.0.0.1"

    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_settings = TestSettings()
