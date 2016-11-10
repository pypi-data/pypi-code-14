import hashlib

from ext.redis_connection import redis_connection_from_env

class RedisSet:

  def __init__(self, name_space='default'):
    self.redis = redis_connection_from_env()
    self.redis_key = name_space + ':set'

  @staticmethod
  def hash(value):
    m = hashlib.sha1()
    m.update(value) 
    return m.digest()

  def add(self, x):
    self.redis.sadd(self.redis_key, self.hash(x))

  def __contains__(self, x):
    #Hash(x) makes this inaccurate but prevents giant URLS from causing problems.
    return self.redis.sismember(self.redis_key, self.hash(x))
