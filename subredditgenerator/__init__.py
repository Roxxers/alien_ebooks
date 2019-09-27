from flask import Flask

# TODO: Before deploying to production, get a way to switch between development and production so that we can run a development server and a production server and not have to edit any docker files.
# TODO: Setup logging for all parts of the server

app = Flask(__name__)
app.config.from_pyfile('config.py')

import praw
from pony.flask import Pony
from flask_restful import Api

from subredditgenerator.cache import Cache

# Setup Reddit Praw client

reddit = praw.Reddit(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    user_agent=app.config["USER_AGENT"]
)

# Wrap all routes (except api endpoints) with db_session
Pony(app)

sub_api = Api(app)


# Setup redis client
cache = Cache(host=app.config["REDIS_HOST"], port=int(app.config["REDIS_PORT"]))

from subredditgenerator import models, routes, api, markov, tasks
