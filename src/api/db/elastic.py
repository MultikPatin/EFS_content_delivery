from elasticsearch import AsyncElasticsearch


class ApiElasticClient:
    """Клиент для работы api с Elastic."""

    def __init__(self, async_client: AsyncElasticsearch):
        self.__async_client = async_client

    def get_async_client(self) -> AsyncElasticsearch:
        return self.__async_client

    async def close(self):
        await self.__async_client.close()


es: ApiElasticClient | None = None


async def get_api_elastic_client() -> ApiElasticClient:
    return es
