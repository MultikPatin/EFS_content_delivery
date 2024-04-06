import asyncio
import time

from elasticsearch import AsyncElasticsearch
import elasticsearch.exceptions

from tests.functional.settings import settings
import backoff


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=elasticsearch.exceptions.ConnectionError,
    max_tries=10,
)
async def ping_check(es_client: AsyncElasticsearch) -> None:
    if not await es_client.ping():
        print("==> Waiting for Elasticsearch")
        raise elasticsearch.exceptions.ConnectionError
    print("----------> Elasticsearch Ready")
    await es_client.close()
    # print("Waiting for Elasticsearch")
    # if await es_client.ping():
    #     print("Elasticsearch Ready")
    #     await es_client.close()
    #     break
    # time.sleep(1)


if __name__ == "__main__":
    client = AsyncElasticsearch(hosts=settings.get_es_host, verify_certs=False)
    asyncio.run(ping_check(client))
    # ioloop = asyncio.get_event_loop()
    # ioloop.run_until_complete(ping_check(client))
    # ioloop.close()
