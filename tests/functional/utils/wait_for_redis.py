import asyncio

from redis.asyncio import Redis

from tests.functional.settings import settings

import backoff
import redis.exceptions


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=redis.exceptions.ConnectionError,
)
async def ping_check(redis_client: Redis) -> None:
    if not await redis_client.ping():
        print("==> Waiting for Redis")
        raise redis.exceptions.ConnectionError
    print("----------> Redis Ready")
    await redis_client.aclose()


if __name__ == "__main__":
    client = Redis(**settings.get_redis_host)

    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(ping_check(client)),
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
