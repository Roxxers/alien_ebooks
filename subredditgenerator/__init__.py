from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config.from_pyfile('config.py')
sub_api = Api(app)

from subredditgenerator import models, routes, api, markov
