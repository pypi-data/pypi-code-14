BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = BROKER_URL
CUBICWEB_CELERYTASK_REDIS_URL = BROKER_URL
CELERY_IMPORTS = ('cw_celerytask_helpers.redislogger', 'demotasks')
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
