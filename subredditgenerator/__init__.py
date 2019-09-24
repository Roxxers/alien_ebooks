from flask import Flask

# TODO: Before deploying to production, get a way to switch between development and production so that we can run a development server and a production server and not have to edit any docker files.

app = Flask(__name__)
app.config.from_pyfile('config.py')

from flask_restful import Api
from flask_apscheduler import APScheduler
from subredditgenerator import cache

scheduler = APScheduler()

sub_api = Api(app)
scheduler.init_app(app)
scheduler.start()

mem_cache = cache.Cache(host=app.config["MEMCACHED_HOST"], port=int(app.config["MEMCACHED_PORT"]))
mem_cache.flush()

from subredditgenerator import models, routes, api, markov, tasks
