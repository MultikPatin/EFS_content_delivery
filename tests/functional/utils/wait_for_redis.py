import asyncio

from redis.asyncio import Redis

from tests.functional.settings import settings
import backoff


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    max_time=10,
)
async def elastic_connect(client: Redis):
    if not await client.ping():
        raise ConnectionError("Connection to Redis failed")


async def main():
    redis = Redis(**settings.get_redis_host)
    print("==> Connecting to Redis ...")
    try:
        await elastic_connect(redis)
    finally:
        await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
