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

"""Models for database ORM"""

from pony import orm

from alien_ebooks import app

db = orm.Database()
db.bind(
    provider=app.config["DB_ENGINE"],
    user=app.config["DB_USER"],
    password=app.config["DB_PASSWORD"],
    host=app.config["DB_HOST"],
    database=app.config["DB_DATABASE"],
    port=app.config["DB_PORT"]
)


class Subreddit(db.Entity):
    """
    Subreddit - Entity for a single subreddit
    """
    id = orm.PrimaryKey(int)
    name = orm.Required(str, unique=True)
    titles = orm.Set("Titles")
    nsfw_percentage = orm.Optional(float)


class Titles(db.Entity):
    """
    Titles - Entity for a reddit submission
    """
    id = orm.PrimaryKey(int)
    subreddit = orm.Required(Subreddit)
    title = orm.Required(str)
    number_of_comments = orm.Required(int)
    nsfw = orm.Required(bool)


db.generate_mapping(create_tables=True)
