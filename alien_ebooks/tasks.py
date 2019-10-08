
import datetime

from flask_apscheduler import APScheduler
from pony.orm import db_session, select

from alien_ebooks import app, cache, models


CLEAR_CACHE_RATE = 1
HOURS_TO_STORE_CACHE = 6

# Setup APScheduler and make it flask compatible
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='clear_cache', hours=CLEAR_CACHE_RATE, misfire_grace_time=900)
def clean_cache():
    now = datetime.datetime.utcnow()
    with db_session:
        subreddits = select(s.name for s in models.Subreddit)[:]

    for subreddit in subreddits:
        value = cache.accesslog_get(subreddit)
        # Check if value is not none as if it is, the accesslog for this subreddit doesn't exist
        # Therefore nothing needs to be done as it hasn't been accessed.
        if value:
            if (now - value) > datetime.timedelta(hours=HOURS_TO_STORE_CACHE):
                cache.delete(subreddit)
                cache.accesslog_delete(subreddit)

@db_session
def delete_former_session_cache():
    subreddits = select(s.name for s in models.Subreddit)[:]
    for subreddit in subreddits:
        cache.delete(subreddit)
