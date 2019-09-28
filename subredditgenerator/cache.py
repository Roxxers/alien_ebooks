
import datetime
import pickle

import redis

from subredditgenerator import config


class Cache:
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port, db=1)
        self.time_of_access = {}
        self.datetime_str = "%Y-%m-%dT%H:%M:%S"
        self.key_append_log = "_accessed_at"
        
    @staticmethod
    def p_value(value):
        return pickle.dumps(value)
    
    @staticmethod
    def unp_value(value):
        return pickle.loads(value)
    
    def _dt_to_str(self, dt):
        return dt.strftime(self.datetime_str)
    
    def _str_to_dt(self, str_obj):
        if isinstance(str_obj, bytes):
            str_obj = str(str_obj, "UTF-8")  # Make sure this is a string
        dt = datetime.datetime.strptime(str_obj, self.datetime_str)
        return dt
        
    def accesslog_set(self, key):
        # Key is changed to avoid conflict with other keys that might use the subreddit name
        new_key = key + self.key_append_log
        now = datetime.datetime.utcnow()
        dt = self._dt_to_str(now)
        return self.client.set(new_key, dt)
    
    def accesslog_get(self, key):
        # Key is changed to avoid conflict with other keys that might use the subreddit name
        new_key = key + self.key_append_log
        value = self.client.get(new_key)
        if value:
            return self._str_to_dt(value)
        else:
            return None
    
    def accesslog_delete(self, key):
        new_key = key + self.key_append_log
        return self.delete(new_key)

    def get(self, key):
        pickled_value = self.client.get(key)
        try:
            value = self.unp_value(pickled_value)
            self.accesslog_set(key)
            return value
        except TypeError:
            # No object at key, return None
            return None

    def set(self, key, value):
        pickled_value = pickle.dumps(value)
        accepted = self.client.set(key, pickled_value)
        self.accesslog_set(key)
        return accepted

    def delete(self, key):
        return self.client.delete(key)
