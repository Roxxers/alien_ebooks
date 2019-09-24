from flask import session, redirect, request, url_for, jsonify, render_template, abort
from subredditgenerator import app


@app.route("/")
def index():
    return render_template("index.html")




    
    #@db_session
    #def post(self, name):
    #    subreddit = reddit.subreddit(name)
    #    db_sub = models.Subreddit(name=subreddit.display_name.lower())
    #    for submission in subreddit.top(limit=None):
    #        models.Titles(id=int(submission.id, 36), title=submission.title, subreddit=db_sub)