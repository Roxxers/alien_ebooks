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
    # TODO: Add debug code here
    self.update_state(
        state="STARTED", meta={'status': "Started requesting data..."}
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
            "finished": False
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

    except TransactionIntegrityError as e:
        # TODO: Add logging error here
        pass
