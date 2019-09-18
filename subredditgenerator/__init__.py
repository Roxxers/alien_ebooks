from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.py')

from flask_restful import Api

sub_api = Api(app)

from subredditgenerator import models, routes, api
