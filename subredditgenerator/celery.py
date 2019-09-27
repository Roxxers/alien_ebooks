from celery import Celery
from subredditgenerator import config, models, reddit

from pony.orm import db_session

celery = Celery('tasks', broker=f"{config.REDIS_URI}0", backend=f"{config.REDIS_URI}0")


@celery.task
@db_session
def add_titles_to_db(subreddit_name: str):
    # TODO: Add debug code here
    # TODO: Add code to be able to get back progress on this process.
    subreddit = reddit.subreddit(subreddit_name)
    db_sub = models.Subreddit(id=int(subreddit.id, 36), name=subreddit.display_name.lower())
    for submission in subreddit.top(limit=None):
        models.Titles(id=int(submission.id, 36), title=submission.title, subreddit=db_sub)