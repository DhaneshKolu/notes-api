import redis

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True,
)
import os
import redis
from redis.exceptions import RedisError

REDIS_URL = os.getenv("REDIS_URL")

redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True
        )
        redis_client.ping()
    except RedisError:
        redis_client = None
