
import datetime
import pickle

from subredditgenerator import config

import redis


class Cache:
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port, db=1)
        self.time_of_access = {}

    def get(self, key):
        pickled_value = self.client.get(key)
        try:
            value = pickle.loads(pickled_value)
            self.time_of_access[key] = datetime.datetime.now()
            return value
        except TypeError:
            return None

    def set(self, key, value):
        pickled_value = pickle.dumps(value)
        accepted = self.client.set(key, pickled_value)
        self.time_of_access[key] = datetime.datetime.now()
        return accepted

    def delete(self, key):
        return self.client.delete(*key)
