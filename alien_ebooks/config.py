import os
from os.path import dirname, join

from dotenv import load_dotenv

app_name = "alien_ebooks"
INFO = {"app_name": app_name}

# We load the env file for when the program is run from source rather than docker.
env_file = ".env"
dotenv_path = join(dirname(__file__), "../", env_file)
load_dotenv(dotenv_path=dotenv_path)

USING_DOCKER = os.getenv("EBOOKS_USING_DOCKER")

DB_ENGINE = "postgres"
DB_HOST = "db" if USING_DOCKER else os.getenv('POSTGRES_HOST')
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_DATABASE = os.getenv("POSTGRES_DATABASE")
DB_PORT = os.getenv("POSTGRES_PORT")

REDIS_HOST = "redis" if USING_DOCKER else os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_URI = "redis://{}:{}/".format(REDIS_HOST, REDIS_PORT)

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = f"{app_name}. Source Code: https://github.com/roxxers/example"

SCHEDULER_API_ENABLED = True
