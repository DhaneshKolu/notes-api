import redis

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True,
)
def invalidate_user_notes_cache(user_id:int):
    for key in redis_client.scan_iter(f"notes:{user_id}:*"):
        redis_client.delete(key)