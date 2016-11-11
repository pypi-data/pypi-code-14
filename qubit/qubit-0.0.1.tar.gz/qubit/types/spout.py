from functools import lru_cache as cache
from functools import partial
import datetime
from collections import namedtuple
from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.io.celery import queue
from qubit.io.celery import period_task
from qubit.io.celery import task_method
from qubit.types.function import Function
from qubit.types.qubit import Qubit

__all__ = ['Spout']


class Spout(Function):
    prototype = types.Table('spout', [
        ('name', types.varchar),
        ('body', types.text),
        ('closure', types.json),
        ('active', types.boolean),
        ('rate', types.integer)
    ])
    data = namedtuple('data', ['datum', 'ts'])
    manager = QuerySet(prototype)

    @classmethod
    def activate_all(cls):
        list(map(cls.measure,
                 map(cls.format, cls.manager.filter(active=True))))

    @classmethod
    def measure(cls, spout, data=None):
        if not data:
            data = cls.data(datum=cls.activate(spout),
                            ts=datetime.datetime.now())
        sig_name = '%s:%s' % (cls.__name__, spout.name)
        qubits = Qubit.get_flying(sig_name)
        list(map(partial(Qubit.measure, data=data), qubits))
        return True

    @staticmethod
    @partial(period_task, name='spout', period=1)
    @queue.task(filter=task_method)
    def activate_period_task():
        return Spout.activate_all()

    @classmethod
    @cache(100)
    def get_via_name(cls, name):
        return cls.format(cls.manager.get_by(name=name))
