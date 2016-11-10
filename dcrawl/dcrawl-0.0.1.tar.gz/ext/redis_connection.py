import os
import redis

def redis_connection_from_env():
  return redis.StrictRedis(
    host=os.environ['REDIS_HOST'], 
    port=os.environ['REDIS_PORT'], 
    db=int(os.environ['REDIS_DB']))