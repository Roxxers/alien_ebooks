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
    id = orm.PrimaryKey(int)
    name = orm.Required(str, unique=True)
    titles = orm.Set("Titles")
    nsfw_percentage = orm.Optional(float)


class Titles(db.Entity):
    id = orm.PrimaryKey(int)
    subreddit = orm.Required(Subreddit)
    title = orm.Required(str)
    number_of_comments = orm.Required(int)
    nsfw = orm.Required(bool)


db.generate_mapping(create_tables=True)
