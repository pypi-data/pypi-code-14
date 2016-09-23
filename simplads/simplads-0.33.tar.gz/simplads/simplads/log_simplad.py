from collections import namedtuple
from simplads.simplad_monad.namedtuples.delta_overwrite import DeltaOverwrite
from simplads.simplad_monad.namedtuples.bind_args import BindArgs
from simplads.simplad_monad.simplad_base_helper import SimpladBaseHelper
import abc

LogDelta = namedtuple('LogDelta', 'messages listeners')

# delta: [messages], {new_listeners}
# annotation: {listeners}

# bind (func)((wrapped_annotation, unbound), higher_deltas)
#     returns (annotation, unbound), higher_deltas
# unit(i) returns annotation, unbound

class LogSimplad(SimpladBaseHelper):
    @staticmethod
    def initial_annotation(unbound):
        return {}

    @staticmethod
    # returns annotation, overwrite_unbound
    def apply_delta(annotation, delta, unbound):
        listeners = annotation
        messages, new_listeners = delta

        # add any new listeners
        for l in new_listeners:
            listeners[l['key']] = (l['func'], l['initial_value'])

        # send any new messages
        def add_message(l, message):
            messages = l[0](l[1], message)
            return (l[0], messages)
        def add_messages(l):
            for message in messages:
                l = add_message(l, message)
            return l
        listeners = {k: add_messages(v) for k, v in listeners.iteritems()}

        return listeners, DeltaOverwrite()

    @staticmethod
    def merge_deltas(a, b):
        return a.messages + b.messages, a.listeners + b.listeners

class LogDeltaMaker():
    @staticmethod
    def messages(messages):
        return LogDelta(messages=messages, listeners=[])

    @staticmethod
    def messages_and_listener(messages):
        def add_to_log(log, message):
            log.append(message)
            return log
        return LogDelta(messages=messages, listeners=[{
            'key': 'log',
            'func': add_to_log,
            'initial_value': []
        }])
