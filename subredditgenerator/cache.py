
import datetime
import pickle

from pymemcache.client import base


class Cache:
    def __init__(self, host: str="localhost", port: int=11211):
        self.client = base.Client((host, port))
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
        try:
            pickled_value = pickle.dumps(value)
            accepted = self.client.set(key, pickled_value)
            self.time_of_access[key] = datetime.datetime.now()
            print("added gssp to cache")
            return accepted
        except:
            return False
        
    def delete(self, key):
        return self.client.delete(key)
    
    def flush(self):
        return self.client.flush_all()
