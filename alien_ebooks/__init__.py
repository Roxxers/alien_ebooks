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

"""alien_ebooks"""

import praw
from flask import Flask
from pony.flask import Pony

from alien_ebooks.cache import Cache

# TODO: Before deploying to production, get a way to switch between development and production so that we can run a development server and a production server and not have to edit any docker files.
# TODO: Setup logging for all parts of the server
# TODO: Download fontawesome svgs and attrib

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Setup Reddit praw client

reddit = praw.Reddit(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    user_agent=app.config["USER_AGENT"]
)

# Wrap all routes (except api endpoints) with db_session
Pony(app)

# Setup redis client
cache = Cache(
    host=app.config["REDIS_HOST"], port=int(app.config["REDIS_PORT"])
)

from alien_ebooks import api, markov, models, routes, tasks
