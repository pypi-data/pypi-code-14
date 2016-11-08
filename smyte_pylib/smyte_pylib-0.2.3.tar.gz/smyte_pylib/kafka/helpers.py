from confluent_kafka_smyte import (
    Consumer,
    KafkaError,
    KafkaException,
    Producer,
    TopicPartition,
)

OFFSET_RESET_OPTIONS = [
    'smallest',
    'earliest',
    'largest',
    'latest',
    'error',
]

# @NOTE: Consumer can get stuck if this is hit. Need to investigate.
PRODUCE_TIMEOUT_MS = 300000

# Only queue 4mb per consumer; much more than this and simple tailers start
# getting expensive memory-wise if there is a backlog. This will probably need
# to be raised to delay with faster consumers
DEFAULT_CONSUMER_QUEUE_MAX_KB = 4 * 1024

BASE_CONFIG = {
    'socket.keepalive.enable': True,

    # We expect a new version of kafka
    'api.version.request': True,

    # Kafka 0.9 closes idle connections waay too quickly.
    # Turn off logging closed connections for now.
    'log.connection.close': False,
}

def _delivery_check_okay(err, msg):
    if err:
        raise KafkaException(err)

def get_consumer(
    config={},
    group_id=None,
    auto_commit=False,
    offset_reset=None,
):
    if offset_reset is None:
        offset_reset = 'error'

    return Consumer(**{
        **BASE_CONFIG,
        'group.id': group_id,
        'enable.auto.commit': auto_commit,
        'queued.max.messages.kbytes': DEFAULT_CONSUMER_QUEUE_MAX_KB,
        'default.topic.config': {
            'auto.offset.reset': offset_reset,
        },
        **config,
    })

def get_producer(config={}):
    return Producer(**{
        **BASE_CONFIG,
        'on_delivery': _delivery_check_okay,
        'default.topic.config': {
            'message.timeout.ms': PRODUCE_TIMEOUT_MS,
        },
        **config,
    })

def topic_partition(topic, partition, offset=None):
    'Create a topic partition object'
    kv = {}
    # Hack to only provide offset kv if it is not None
    if offset is not None:
        kv['offset'] = offset
    return TopicPartition(
        topic=topic,
        partition=partition,
        **kv
    )
