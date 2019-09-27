

from flask import (abort, jsonify, redirect, render_template, request, session,
                   url_for)

from subredditgenerator import app, reddit
from subredditgenerator.models import Subreddit, Titles


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_subreddit/<subreddit_name>")
def create_subreddit(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    
    return "hello"
