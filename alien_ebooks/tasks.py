# alien_ebooks
# Copyright (C) 2019  Roxanne Gibson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""APScheduler tasks for running scheduled background tasks."""

import datetime

from flask_apscheduler import APScheduler
from pony.orm import db_session, select

from alien_ebooks import app, cache, models

CLEAR_RATE = 1
HOURS_TO_STORE_CACHE = 6

# Setup APScheduler and make it flask compatible
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


@scheduler.task(
    'interval', id='clear_cache', hours=CLEAR_RATE, misfire_grace_time=900
)
def clean_cache():
    """clean_cache - checks cache and clears data that has exceeded the maximum amount of time in the cache."""
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
    """delete_former_session_cache - deletes redis db data from previous sessions"""
    subreddits = select(s.name for s in models.Subreddit)[:]
    for subreddit in subreddits:
        cache.delete(subreddit)
