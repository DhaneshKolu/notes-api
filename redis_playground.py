import redis
import time
r = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True
)



def get_data(key):
    cached = r.get(key)
    if(cached):
        print("CACHE HIT")
        return cached
    print("CACHE MISS")
    value = "data from database"
    r.setex(key,15,value)
    return value

print(get_data("notes_page_1"))
print(get_data("notes_page_1"))