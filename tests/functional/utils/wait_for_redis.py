import time

from redis.asyncio import Redis

from tests.functional.settings import test_settings

if __name__ == "__main__":
    client = Redis(**test_settings.get_redis_host)
    while True:
        if client.ping():
            break
        time.sleep(1)
