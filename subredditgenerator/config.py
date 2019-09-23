import configparser

file = configparser.ConfigParser()
file.read("subredditgen.conf")


DB_ENGINE = file["db"]["db_engine"]
DB_HOST = file["db"]["host"]
DB_USER = file["db"]["user"]
DB_PASSWORD = file["db"]["password"]
DB_DATABASE = file["db"]["database"]


CLIENT_ID = file["reddit"]["client_id"]
CLIENT_SECRET = file["reddit"]["client_secret"]
USER_AGENT = file["reddit"]["user_agent"]

SCHEDULER_API_ENABLED = True