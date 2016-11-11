from qubit.config import MQ_BROKER, REDIS_BACKEND

TIMEZONE = 'Europe/London'
ENABLE_UTC = True
BROKER_URL = MQ_BROKER
CELERY_RESULT_BACKEND = REDIS_BACKEND
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.
CELERY_ALWAYS_EAGER = False
CELERY_DEFAULT_QUEUE = 'qubit.tasks.default'
CELERY_DEFAULT_EXCHANGE = 'qubit.tasks.default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
# These settings is used for fix `celeryev.xxx queue huge length` problem:
# http://stackoverflow.com/questions/30227266/what-is-the-celeryev-queue-for
# http://stackoverflow.com/questions/17778715/celeryev-queue-in-rabbitmq-becomes-very-large
# DOC:
# http://celery.readthedocs.io/en/latest/configuration.html#celery-event-queue-ttl
CELERY_SEND_EVENTS = True
CELERY_EVENT_QUEUE_TTL = 60
CELERY_EVENT_QUEUE_EXPIRES = 60  # Will delete all celeryev. queues without consumers after 1 minute.
