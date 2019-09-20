
from pymemcache.client import base
import pickle


class Cache:
    def __init__(self, host="localhost", port=11211):
        self.client = base.Client((host, port))
    
    def get(self, key):
        pickled_value = self.client.get(key)
        try:
            return pickle.loads(pickled_value)
        except TypeError:
            return False

    def set(self, key, value):
        pickled_value = pickle.dumps(value)
        return self.client.set(key, pickled_value)
