from pydantic.fields import Field
from pydantic_settings import BaseSettings


class ElasticSettings(BaseSettings):
    """
    This class is used to store the Elastic connection settings.
    """

    host: str = Field(default=..., alias="ELASTIC_HOST")
    port: int = Field(default=9200, alias="ELASTIC_PORT")

    @property
    def get_host(self) -> str:
        return f"http://{self.host}:{self.port}"
