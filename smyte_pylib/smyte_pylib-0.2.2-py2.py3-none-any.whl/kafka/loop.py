from __future__ import absolute_import

import logging
from confluent_kafka_smyte import (
    KafkaError,
    KafkaException,
    TopicPartition,
)

from .helpers import get_consumer
from ..main_loop import main_loop

logger = logging.getLogger('pylib.seqconsumer')

class KafkaLoop:
    def __init__(
        self,
        topic,
        group,
        auto_commit=False,
        parse=False,
        offset_reset='error',
        consumer_config={},
    ):
        self.topic = topic
        self.group = group
        self.auto_commit = auto_commit
        self.offset_reset = offset_reset
        self.parse = parse
        self.consumer_config = consumer_config
        self._consumer = None

    def commit_next_offset(self, topic, partition, next_offset, async=True):
        assert self._consumer, 'Kafka loop is not currently running'
        self._consumer.commit(
            offsets=[TopicPartition(
                topic=topic,
                partition=partition,
                offset=next_offset,
            )],
            async=async,
        )

    def commit_message(self, message, async=True):
        self.commit_next_offset(
            topic=message.topic(),
            partition=message.partition(),
            offset=message.offset() + 1,
            async=async,
        )

    def run(self, handler):
        self._consumer = get_consumer(
            config=self.consumer_config,
            group_id=self.group,
            auto_commit=self.auto_commit,
            offset_reset=self.offset_reset,
        )

        def on_assign(consumer, assignments):
            partitions = [topic_partition.partition for topic_partition in assignments]
            logger.info('Consuming from partitions: %s' % ', '.join(map(str, partitions)))
            handler.reset()
            handler.assign_partitions([
                (topic_partition.topic, topic_partition.partition)
                for topic_partition in assignments
            ])

        def on_revoke(consumer, assignments):
            partitions = [topic_partition.partition for topic_partition in assignments]
            logger.info('Revoked partitions: %s' % ', '.join(map(str, partitions)))
            handler.revoke_partitions([
                (topic_partition.topic, topic_partition.partition)
                for topic_partition in assignments
            ])

        self._consumer.subscribe(
            [self.topic],
            on_assign=on_assign,
            on_revoke=on_revoke,
        )

        def inner():
            msg = self._consumer.poll(timeout=1.0)
            if msg is None:
                handler.no_message()
                return

            error = msg.error()
            if error:
                if error.code() == KafkaError._PARTITION_EOF:
                    handler.process_eof(msg.topic(), msg.partition())
                    logger.debug('%% %s [%d] reached end at offset %d\n' % (
                        msg.topic(), msg.partition(), msg.offset()
                    ))
                    return

                raise KafkaException(error)

            handler.process_message(
                topic=msg.topic(),
                partition=msg.partition(),
                offset=msg.offset(),
                timestamp_ms=msg.timestamp(),
                key=msg.key(),
                value=msg.value(),
            )

        try:
            main_loop(inner)
        finally:
            self.stop()

    def stop(self):
        if self._consumer:
            self._consumer.close()
            self._consumer = None
