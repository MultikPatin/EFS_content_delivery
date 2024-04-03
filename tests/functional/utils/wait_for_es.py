import time

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings

if __name__ == "__main__":
    client = AsyncElasticsearch(hosts=settings.get_es_host, verify_certs=False)
    while True:
        print("Waiting for Elasticsearch")
        if client.ping():
            break
        time.sleep(1)
