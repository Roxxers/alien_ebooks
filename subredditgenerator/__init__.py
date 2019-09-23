from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from flask_restful import Api
from flask_apscheduler import APScheduler
from subredditgenerator import cache

scheduler = APScheduler()

sub_api = Api(app)
scheduler.init_app(app)
scheduler.start()

mem_cache = cache.Cache()
mem_cache.flush()

from subredditgenerator import models, routes, api, markov, tasks
