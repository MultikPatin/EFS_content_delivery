import asyncio

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings
import backoff


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    max_time=10,
)
async def elastic_connect(client: AsyncElasticsearch):
    if not await client.ping():
        raise ConnectionError("Connection failed")


async def main():
    elastic = AsyncElasticsearch(hosts=settings.get_es_host, verify_certs=True)
    print("==> Connecting to Elasticsearch ...")
    try:
        await elastic_connect(elastic)
    finally:
        await elastic.close()


if __name__ == "__main__":
    asyncio.run(main())
