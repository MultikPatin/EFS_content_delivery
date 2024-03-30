from pydantic.fields import Field
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    """
    This class is used to store the REDIS connection settings.
    """

    host: str = Field(default=..., alias="REDIS_HOST")
    port: int = Field(default=6379, alias="REDIS_PORT")
