import time

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings

if __name__ == "__main__":
    client = AsyncElasticsearch(
        hosts=test_settings.get_es_host, verify_certs=False
    )
    while True:
        if client.ping():
            break
        time.sleep(1)
