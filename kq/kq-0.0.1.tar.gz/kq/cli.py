"""
Start a KQ worker

Usage:
  kq-worker [--hosts=<hosts>]
            [--topic=<topic>]
            [--timeout=<timeout>]
            [--sync]
            [--rdkafka]
  kq-worker --help
  kq-worker --version

Options:
  --hosts=<hosts>      Comma separated Kafka host names & ports
  --topic=<topic>      The name of the Kafka topic
  --timeout=<timeout>  The job timeout threshold in seconds
  --sync               Quarantine failed jobs synchronously
  --rdkafka            Use the librdkafka C library
  --help               Display this help menu
  --version            Display the version of KQ
"""

import logging

import docopt

from kq import VERSION
from kq import Worker


def entry_point():
    logger = logging.getLogger('kq.worker')
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    ))
    logger.addHandler(stream_handler)

    args = docopt.docopt(__doc__, version=VERSION)

    if args['--hosts'] is None:
        kafka_hosts = ['127.0.0.1:9092']
    else:
        kafka_hosts = args['--hosts'].split(',')

    worker = Worker(
        hosts=kafka_hosts,
        topic=args['--topic'],
        sync=args['--sync'],
        timeout=args['--timeout'],
        rdkafka=args['--rdkafka'],
    )
    worker.start()
