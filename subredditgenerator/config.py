	
import os
from os.path import join, dirname
from dotenv import load_dotenv
 
# We load the env file for when the program is run from source rather than docker.
env_file = ".env" 
dotenv_path = join(dirname(__file__), env_file)
load_dotenv(dotenv_path)

USING_DOCKER = os.getenv("SUBREDDIT_USING_DOCKER", False)

DB_ENGINE = "postgres"
DB_HOST = "postgres" if USING_DOCKER else os.getenv('POSTGRES_HOST')
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_DATABASE = os.getenv("POSTGRES_DATABASE")
DB_PORT = os.getenv("POSTGRES_PORT")


MEMCACHED_HOST = "memcached" if USING_DOCKER else os.getenv("MEMCACHED_HOST")
MEMCACHED_PORT = os.getenv("MEMCACHED_PORT")


CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = "Subreddit Generator. Source Code by u/rainbowroxxers"

SCHEDULER_API_ENABLED = True