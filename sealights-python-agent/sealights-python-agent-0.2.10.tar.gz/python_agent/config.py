import os


os.environ["COVERAGE_WTW"] = "1"  # who-what-where environment variable for coverage per test from coverage.py
DEFAULT_BUILD = "1"
DEFAULT_BRANCH = "master"
DEFAULT_ENV = "Unit Tests"
TEST_IDENTIFIER = "x-sl-testid"
CONTEXT_MATCH = None


PYTHON_FILES_REG = r"^[^.#~!$@%^&*()+=,]+\.pyw?$"  # regex taken from coverage.py for finding python files
INIT_TEST_NAME = "__init"
INITIAL_COLOR = "00000000-0000-0000-0000-000000000000/__init"
MAX_ITEMS_IN_QUEUE = 5000
INTERVAL_IN_MILLISECONDS = 30000

FOOTPRINTS_ROUTE_VERSION = "v2"
FOOTPRINTS_ROUTE = "/" + FOOTPRINTS_ROUTE_VERSION + "/testfootprints"
BUILD_MAPPING_ROUTE_VERSION = "v1"
BUILD_MAPPING_ROUTE = "/" + BUILD_MAPPING_ROUTE_VERSION + "/buildmapping"
TEST_EVENTS_ROUTE_VERSION = "v1"
TEST_EVENTS_ROUTE = "/" + TEST_EVENTS_ROUTE_VERSION + "/testevents"
LOG_SUBMISSION_ROUTE_VERSION = "v1"
LOG_SUBMISSION_ROUTE = "/" + LOG_SUBMISSION_ROUTE_VERSION + "/logsubmission"
TEST_EXECUTION_ROUTE_VERSION = "v2"
TEST_EXECUTION_ROUTE = "/" + TEST_EXECUTION_ROUTE_VERSION + "/testExecution"
EXTERNAL_DATA_ROUTE_VERSION = "v2"
EXTERNAL_DATA_ROUTE = "/" + EXTERNAL_DATA_ROUTE_VERSION + "/externaldata"

app = {
    "customer_id": None,
    "app_name": None,
    "build": DEFAULT_BUILD,
    "branch": DEFAULT_BRANCH,
    "server": None,
    "proxy": None,
    "technology": "python",
    "env": DEFAULT_ENV,
    "test_phase": None,
    "is_initial_color": False
}

LOG_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'sealights-standard': {
            'format': '%(asctime)s %(levelname)s [%(process)d|%(thread)d] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'sealights-console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG' if os.environ.get("SL_DEBUG") else 'INFO',
            'formatter': 'sealights-standard',
            'stream': 'ext://sys.stdout',
        },
        'sealights-file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG' if os.environ.get("SL_DEBUG") else 'INFO',
            'formatter': 'sealights-standard',
            'filename': '/tmp/sealights-python-agent.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        }
    },
    'loggers': {
        'python_agent': {
            'handlers': ['sealights-file'] if os.environ.get("SL_DEBUG") else [],
            'level': 'DEBUG' if os.environ.get("SL_DEBUG") else 'INFO',
            'propagate': False
        },
        'python_agent.packages.requests.packages.urllib3.connectionpool': {
            'handlers': [],
            'level': 'WARN',
            'propagate': False
        },
        'apscheduler': {
            'handlers': [],
            'level': 'CRITICAL',
            'propagate': False
        },
        'pip': {
            'handlers': [],
            'level': 'WARN',
            'propagate': False
        }
    }
}

FUTURE_STATEMENTS = {
    "nested_scopes": 0x0010,
    "generators": 0,
    "division": 0x2000,
    "absolute_import": 0x4000,
    "with_statement": 0x8000,
    "print_function": 0x10000,
    "unicode_literals": 0x20000,
}

