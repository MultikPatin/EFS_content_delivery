import time

from redis.asyncio import Redis

from tests.functional.settings import settings

if __name__ == "__main__":
    client = Redis(**settings.get_redis_host)
    while True:
        print("Waiting for Redis")
        if client.ping():
            break
        time.sleep(1)
