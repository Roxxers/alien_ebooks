from subredditgenerator import app
from pony import orm


db = orm.Database()
db.bind(
    provider=app.config["DB_ENGINE"],
    user=app.config["DB_USER"],
    password=app.config["DB_PASSWORD"],
    host=app.config["DB_HOST"],
    database=app.config["DB_DATABASE"]
    )


class Subreddit(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)
    titles = orm.Set("Titles")


class Titles(db.Entity):
    id = orm.PrimaryKey(int)
    subreddit = orm.Required(Subreddit)
    title = orm.Required(str)


db.generate_mapping(create_tables=True)
