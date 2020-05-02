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

"""Celery module for tasks to be run in the background for the web app."""

import time
from celery import Celery
from pony.orm import db_session, TransactionIntegrityError

from alien_ebooks import config, models, reddit

celery = Celery(
    'background_tasks',
    broker=f"{config.REDIS_URI}0",
    backend=f"{config.REDIS_URI}0"
)


@celery.task(bind=True)
@db_session
def add_titles_to_db(self, subreddit_name: str):
    """add_titles_to_db - scrapes a subreddit and posts to the database

    Args:
        subreddit_name (str): name of subreddit to add posts from
    """
    # TODO: Add debug code here
    self.update_state(
        state="STARTED",
        meta={
            'status': "Started requesting data...",
            "subreddit": subreddit_name
        }
    )
    subreddit = reddit.subreddit(subreddit_name)
    try:
        amount_of_posts = 1000 # This is around the limit given by the api, just an estimate
        # Set amount of processed posts and update state of task for api
        processed = 0
        meta = {
            "status": "Processing data",
            "total": amount_of_posts,
            "current": processed,
            "finished": False,
            "subreddit": subreddit_name
        }
        self.update_state(state="PROCESSING", meta=meta)

        # Add subreddit to subreddit table to setup the one to many link
        db_sub = models.Subreddit(
            id=int(subreddit.id, 36), name=subreddit.display_name.lower()
        )

        # Iterate through all posts we can get and add them to the database, incrementing status and processed each time
        for submission in subreddit.top(limit=None):
            models.Titles(
                id=int(submission.id, 36),
                title=submission.title,
                subreddit=db_sub,
                number_of_comments=submission.num_comments,
                nsfw=bool(submission.over_18)
            )
            meta["current"] += 1
            self.update_state(state="PROCESSING", meta=meta)
        meta["finished"] = True
        self.update_state(state="FINISHED", meta=meta)
        # Added sleep to give client's time to see that the task is completed before it is deleted from the queue.
        time.sleep(5)

    except TransactionIntegrityError as e:
        # TODO: Add logging error here
        pass
