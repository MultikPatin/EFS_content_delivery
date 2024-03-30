import logging
from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from redis.asyncio import Redis

from src.api.core.config import settings
from src.api.core.logger import LOGGING
from src.api.db import elastic, redis
from src.api.db.elastic import ApiElasticClient
from src.api.db.redis import ApiRedisClient
from src.api.endpoints.v1 import films, genres, persons
from src.core.utils.logger import create_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.api_redis_client = ApiRedisClient(
        Redis(host=settings.redis.host, port=settings.redis.port),
        logger=create_logger("API RedisClient"),
    )
    elastic.es = ApiElasticClient(
        async_client=AsyncElasticsearch(hosts=settings.elastic.get_host),
    )
    yield
    await redis.api_redis_client.close()
    await elastic.es.close()


app = FastAPI(
    title=settings.name,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
