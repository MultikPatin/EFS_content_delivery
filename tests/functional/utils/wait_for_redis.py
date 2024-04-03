import asyncio
import time

from redis.asyncio import Redis

from tests.functional.settings import settings


async def ping_check(redis_client: Redis) -> None:
    while True:
        print("Waiting for Redis")
        if await redis_client.ping():
            print("Redis Ready")
            await redis_client.aclose()
            break
        time.sleep(1)


if __name__ == "__main__":
    client = Redis(**settings.get_redis_host)

    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(ping_check(client)),
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
