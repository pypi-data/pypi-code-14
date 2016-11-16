HTTP_PORT = 8000
HTTP_HOST = '127.0.0.1'

TMP_DIR = 'tmp/'

MYSQL_HOSTS = {}

# MYSQL_SHARDS is used to know where data lives
MYSQL_SHARDS = {}

MYSQL_SSH_PORT = 22

MAX_CRATE_RESULT_SIZE = 100000

CRATE_CLUSTERS = {}
CRATE_SHARDS = {}
CRATE_HTTP_PORT = 4200
CRATE_TCP_PORT = 4300

SOURCES = {}
DESTINATIONS = {}

SHARD_TABLES = None
MYSQL_SHARD_TABLES = None
CRATE_SHARD_TABLES = None

CRATE_SSH_PORT = 2222

CHUNK_SIZE = 100000
SSH_USER = None

ENABLE_VERIFIER = True
VERIFICATION_DELAY = 5
RUN_IMPORT_WORKERS = True
ENABLE_ARCHIVER = True
INLINE_TRIMMING = False

SHARD_SUFFIXES = {
    'default': '',
}

PIPE_BULK_INSERT_SIZE = 1000

# Seconds to subtract from the beginning of a delta start to make sure we're getting any potential crossover data.
# Also used to check if any new data has come in during a migration.
# This should be able to be 0 as long as the source_start_time is used, but better to be safe.
DELTA_START_FUDGE_FACTOR = 30
# Seconds to subtract from the earliest start_time if no source_start_time can be found. The start_time may have been
# calculated from a different time zone from the DB server and the clocks may have drifted, so best to use 1 day
# for safety.
DELTA_START_FUDGE_FACTOR_FALLBACK = 60 * 60 * 24

PARTITION_SPECIFIC_TRIMMING_THRESHOLDS = {}

# NOTE: This is per MySQL shard
NUM_EXPORT_WORKERS = 2
NUM_PIPE_WORKERS = 2
NUM_QUEUE_MIGRATION_WORKERS = 2

NUM_STREAM_WORKERS = 2
NUM_ARCHIVE_WORKERS = NUM_STREAM_WORKERS
NUM_IMPORT_WORKERS = 4
NUM_VERIFICATION_WORKERS = 2

# If set to True, constraint failures during upserts will cause the worker to retry each record individually and ignore
# those that cause constraint failures.
IGNORE_CONSTRAINT_FAILURES = False

LOGGING_INI = None
SSH_PRIVKEY = None
HDFS_ENDPOINT = None
HDFS_USER = None
HDFS_PATH = None

QUEUE_SYSTEM = 'celery'

# Celery
CELERY_BROKER = None
