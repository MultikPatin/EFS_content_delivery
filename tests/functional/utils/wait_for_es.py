import asyncio
import time

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings


async def ping_check(es_client: AsyncElasticsearch) -> None:
    while True:
        print("Waiting for Elasticsearch")
        if await es_client.ping():
            print("Elasticsearch Ready")
            await es_client.close()
            break
        time.sleep(1)


if __name__ == "__main__":
    client = AsyncElasticsearch(hosts=settings.get_es_host, verify_certs=False)

    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(ping_check(client)),
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
