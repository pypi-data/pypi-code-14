from datetime import datetime
from hashlib import sha1
from rask.base import Base
from rask.parser.json import dictfy
from rask.rmq import ack

__all__ = ['Cronpoke']

class Cronpoke(Base):
    __events = None
    __queue = None
    options = {
        'actions':[
            'for_each_hour',
            'for_each_minute'
        ],
        'rmq_exchange':'cronpoke'
    }

    @property
    def __events__(self):
        try:
            assert self.__events
        except AssertionError:
            self.__events = {
                'for_each_hour':[],
                'for_each_minute':[]
            }
        except:
            raise
        return self.__events

    @property
    def queue(self):
        try:
            assert self.__queue
        except AssertionError:
            self.__queue = sha1('%s:%s' % (self.uuid,self.ioengine.uuid4)).hexdigest()
        except:
            raise
        return self.__queue

    def __declare__(self,channel):
        def on_msg(channel,method,properties,body):
            try:
                self.ioengine.loop.add_callback(
                    self.__trigger_events__,
                    cb=self.__events__[properties.headers['action']],
                    date=datetime.strptime(dictfy(body)['date'],'%Y-%m-%dT%H:%M:%S.%f'),
                    ack=ack(channel,method)
                )
            except (KeyError,TypeError):
                channel.basic_ack(method.delivery_tag)
            except:
                raise
            return True

        def on_declare(*args):
            for action in self.options['actions']:
                channel.queue_bind(
                    callback=None,
                    exchange=self.options['rmq_exchange'],
                    queue=self.queue,
                    routing_key='',
                    arguments={
                        'service':'cronpoke',
                        'action':action,
                        'x-match':'all'
                    }
                )

            channel.basic_consume(
                consumer_callback=on_msg,
                queue=self.queue
            )
            self.log.info('Listening')
            return True

        channel.queue_declare(
            callback=on_declare,
            auto_delete=True,
            exclusive=True,
            durable=False,
            queue=self.queue
        )
        return True

    def __init__(self,rmq):
        self.rmq = rmq
        self.ioengine.loop.add_callback(self.__services__)

    def __services__(self):
        def declare(_):
            self.ioengine.loop.add_callback(
                self.__declare__,
                channel=_.result().channel
            )
            return True

        self.rmq.channel('rask_cronpoke_%s' % self.uuid,self.ioengine.future(declare))
        return True

    def __trigger_events__(self,cb,date,ack,i=0):
        try:
            self.ioengine.loop.add_callback(cb[i],date)
        except IndexError:
            ack(True)
        except:
            raise
        else:
            self.ioengine.loop.add_callback(
                self.__trigger_events__,
                cb=cb,
                date=date,
                ack=ack,
                i=i+1
            )
        return True

    def add_cb_hour(self,cb):
        self.__events__['for_each_hour'].append(cb)
        return True

    def add_cb_minute(self,cb):
        self.__events__['for_each_minute'].append(cb)
        return True
