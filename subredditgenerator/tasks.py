
import datetime
from subredditgenerator import scheduler, mem_cache

CLEAR_CACHE_HOUR = 1
TIME_TO_STORE_CACHE = 6


@scheduler.task('interval', id='clear_cache', hours=CLEAR_CACHE_HOUR, misfire_grace_time=900)
def clear_cache():
    now = datetime.datetime.now()
    
    cache_helper = mem_cache.time_of_access.copy()
    for key, value in cache_helper.items():
        if (now - value) > datetime.timedelta(hours=TIME_TO_STORE_CACHE):
            mem_cache.delete(key)
            mem_cache.time_of_access.pop(key)
