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

"""Handles caching python objects in a redis server."""

import datetime
import pickle
from typing import Any, Union

import redis


class Cache:
    """Wrapper for redis server caching to help cache pickled bytes and access
    times."""
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port, db=1)
        self.time_of_access = {}
        self.datetime_str = "%Y-%m-%dT%H:%M:%S"
        self.key_append_log = "_accessed_at"

    def _dt_to_str(self, dt: datetime.datetime) -> str:
        """_dt_to_str - convert datetime to string object to store in redis

        Args:
            dt (datetime.datetime): datetime object to convert

        Returns:
            str: converted datetime
        """
        return dt.strftime(self.datetime_str)

    def _str_to_dt(self, str_obj: Union[str, bytes]) -> datetime.datetime:
        """_str_to_dt - converts string or byte string to datetime object from cache

        Args:
            str_obj (Union[str, bytes]): datetime represented as a string from the cache

        Returns:
            datetime.datetime: converted string
        """
        if isinstance(str_obj, bytes):
            str_obj = str(str_obj, "UTF-8") # Make sure this is a string
        dt = datetime.datetime.strptime(str_obj, self.datetime_str)
        return dt

    def accesslog_set(self, key: str) -> None:
        """accesslog_set - log when a resource was accessed in the cache

        Args:
            key (str): key of the resource accessed
        """
        # Key is changed to avoid conflict with other keys that might use the subreddit name
        new_key = key + self.key_append_log
        now = datetime.datetime.utcnow()
        dt = self._dt_to_str(now)
        self.client.set(new_key, dt)

    def accesslog_get(self, key: str) -> Union[datetime.datetime, None]:
        """accesslog_get - get accesslog datetime for resource

        Args:
            key (str): key of the resource to get last access time of

        Returns:
            Union[datetime.datetime, None]: either datetime of last access of resource or None if doesn't exist.
        """
        # Key is changed to avoid conflict with other keys that might use the subreddit name
        new_key = key + self.key_append_log
        value = self.client.get(new_key)
        if value:
            return self._str_to_dt(value)
        else:
            return None

    def accesslog_delete(self, key: str) -> None:
        """accesslog_delete - deletes accesslog value from cache

        Args:
            key (str): key for value in the redis db
        """
        new_key = key + self.key_append_log
        self.delete(new_key)

    def get(self, key: str) -> Any:
        """get - gets value from redis cache using key

        Args:
            key (str): key for value in the redis db

        Returns:
            Any: obj that has been converted from a bytesarray
        """
        pickled_value = self.client.get(key)
        try:
            value = pickle.loads(pickled_value)
            self.accesslog_set(key)
            return value
        except TypeError:
            # No object at key, return None
            return None

    def set(self, key: str, value: Any) -> None:
        """set - stores pickled obj into cache with the given key

        Args:
            key (str): key for value in the redis db
            value (Any): object to be stored, pickled
        """
        pickled_value = pickle.dumps(value)
        self.client.set(key, pickled_value)
        self.accesslog_set(key)

    def delete(self, key: str) -> None:
        """delete - deletes value from cache

        Args:
            key (str): key for value in the redis db
        """
        self.client.delete(key)
