import collections
import json
import logging
import uuid

import boto3.session

LOGGER = logging.getLogger(__name__)

class Queue(): # pylint: disable=too-few-public-methods
    def __init__(self, queuename, access_key_id=None, secret_access_key=None, region_name=None):
        region_name = region_name or 'us-west-2'
        self.session = boto3.session.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name)

        self.sqs = self.session.resource('sqs')
        self.queue = self.sqs.get_queue_by_name(QueueName=queuename)

    def push(self, credentials, content):
        message = {
            'credentials'   : credentials,
            'content'       : content,
        }
        result = self.queue.send_message(MessageBody=json.dumps(message))
        LOGGER.info("Created message with message ID %s and MD5 %s",
            result.get('MessageId'),
            result.get('MD5OfMessageBody'),
        )
        return result.get('MessageId')

    def messages(self, wait_time_seconds=20):
        for message in self.queue.receive_messages(WaitTimeSeconds=wait_time_seconds):
            yield Message(message)

class Message(): # pylint: disable=too-few-public-methods
    def __init__(self, message):
        self.message = message
        self.body = json.loads(message.body)

    def delete(self):
        return self.message.delete()

    def __getattr__(self, name):
        return getattr(self, name)

class SQSFake(): # pylint: disable=too-few-public-methods
    FakeMessage = collections.namedtuple('FakeMessage', ['body'])
    def __init__(self):
        self.sent_messages = []

    def send_message(self, MessageBody):
        self.sent_messages.append(json.loads(MessageBody))
        return {
            'MessageId'         : uuid.uuid4(),
            'MD5OfMessageBody'  : None,
        }

    def receive_messages(self, WaitTimeSeconds=None): # pylint: disable=unused-argument
        for message in self.sent_messages:
            yield self.FakeMessage(body=json.dumps(message))

class QueueFake(Queue):
    def __init__(self): # pylint: disable=super-init-not-called
        self.queue = SQSFake()

    @property
    def sent_messages(self):
        return self.queue.sent_messages

    def sent(self, message):
        return message in self.sent_messages
