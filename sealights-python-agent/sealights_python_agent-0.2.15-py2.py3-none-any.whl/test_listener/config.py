app = {
    "customer_id": None,
    "app_name": None,
    "build": "1",
    "branch": "master",
    "server": None,
    "proxy": None,
    "technology": "python",
    "env": None
}

TEST_IDENTIFIER = "x-sl-testid"

LOG_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'sealights-standard': {
            'format': '%(asctime)s %(levelname)s [%(process)d|%(thread)d] %(name)s: %(message)s'
        }
    },
    'loggers': {
        'python_agent': {
            'handlers': [],
            'level': 'INFO',
            'propagate': False
        },
        'python_agent.requests.packages.urllib3.connectionpool': {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
