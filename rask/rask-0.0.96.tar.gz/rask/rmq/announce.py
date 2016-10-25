from rask.base import Base
from rask.options import options

__all__ = ['Announce']

class Announce(Base):   
    def __init__(self,channel,settings):
        self.channel = channel.result().channel
        self.settings = settings
        self.ioengine.loop.add_callback(self.exchange_declare)
        self.log.info('started')

    def exchange_declare(self):
        def on_topic(*args):
            self.log.info('Exchange declare: %s' % self.settings['exchange']['topic'])
            return True
        
        def on_headers(*args):
            self.log.info('Exchange declare: %s' % self.settings['exchange']['headers'])
            self.channel.exchange_bind(
                destination=self.settings['exchange']['headers'],
                source=self.settings['exchange']['topic'],
                routing_key='#'
            )
            self.ioengine.loop.add_callback(self.queue_declare)
            return True
        
        self.channel.exchange_declare(
            callback=on_topic,
            exchange=self.settings['exchange']['topic'],
            exchange_type='topic',
            durable=True
        )
        
        self.channel.exchange_declare(
            callback=on_headers,
            exchange=self.settings['exchange']['headers'],
            exchange_type='headers',
            durable=True
        )
        return True

    def queue_declare(self,_=None):
        try:
            service = _.next()

            def on_declare(*args):
                self.channel.queue_bind(
                    callback=None,
                    queue=self.settings['services'][service]['queue'],
                    exchange=self.settings['exchange']['topic'],
                    routing_key=self.settings['services'][service]['rk']
                )
                return True

            self.channel.queue_declare(
                arguments=self.settings['services'][service].get('arguments'),
                callback=on_declare,
                queue=self.settings['services'][service]['queue'],
                durable=True,
                exclusive=False
            )
        except AttributeError:
            self.ioengine.loop.add_callback(
                self.queue_declare,
                iter(self.settings['services'])
            )
        except StopIteration:
            return True
        except:
            raise
        else:
            self.log.info('Queue declare: %s' % self.settings['services'][service]['queue'])
            self.ioengine.loop.add_callback(
                self.queue_declare,
                _=_
            )
        return None

