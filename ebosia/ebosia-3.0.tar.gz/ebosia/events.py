import bz2
import collections
import json

Event = collections.namedtuple('Event', ['topic', 'payload'])

def from_kombu(body, message):
    #topic = message.properties['delivery_info'].get('routing_key')
    topic = message.delivery_info['routing_key']
    return Event(topic, body)

def from_aioamqp(body, envelope, properties): # pylint: disable=unused-argument
    decompressed = bz2.decompress(body)
    decoded = decompressed.decode('utf-8')
    parsed = json.loads(decoded)
    topic = envelope.routing_key
    return Event(topic, parsed)
