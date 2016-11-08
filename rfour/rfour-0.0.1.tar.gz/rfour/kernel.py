import arrow
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import ack,Announce,BasicProperties

__all__ = ['Kernel']

class Kernel(Base):
    __settings = {
        'exchange':{
            'headers':'rfour_headers',
            'topic':'rfour'
        }
    }
    
    def __init__(self,rmq):
        self.rmq = rmq
        self.ch
        
    @property
    def ch(self):
        try:
            assert self.__ch
        except (AssertionError,AttributeError):
            self.__ch = {}
            self.__settings['services'] = {
                'input':{
                    'durable':False,
                    'exclusive':True,
                    'queue':'rfour_input_%s' % self.uuid,
                    'rk':'rfour.input.%s' % self.uuid
                },
                'output':{
                    'durable':False,
                    'exclusive':True,
                    'queue':'rfour_output_%s' % self.uuid,
                    'rk':'rfour.output.%s' % self.uuid
                }
            }
            
            def on_ch_input(_):
                self.__ch['input'] = _.result().channel

                self.channel.basic_consume(
                    consumer_callback=self.__input_on_msg__,
                    queue=self.__settings['services']['input']['queue']
                )
                return True
            
            def on_ch_output(_):
                self.__ch['output'] = _.result().channel
                Announce(_,self.__settings)
                return True
            
            self.rmq.channel(self.__channels__['i'],future=self.ioengine.future(on_ch_input))
            self.rmq.channel(self.__channels__['o'],future=self.ioengine.future(on_ch_output))
        except:
            raise
        return self.ch

    @property
    def datetime_f(self):
        return str(arrow.utcnow().float_timestamp)

    @property
    def etag(self):
        return self.ioengine.uuid4

    @property
    def tasks(self):
        try:
            assert self.__tasks
        except (AssertionError,AttributeError):
            self.__tasks = {}
        except:
            raise
        return self.__tasks
    
    @property
    def utocde(self):
        try:
            assert self.__utcode
        except (AssertionError,AttributeError):
            self.__utcode = UTCode()
        except:
            raise
        return self.__utcode
    
    def __channel__(self,_):
        return '%s_%s' % (self.uuid,_)
        
    def __channels__(self):
        try:
            assert self.__channels
        except (AssertionError,AttributeError):
            self.__channels = {
                'i':self.__channel__('input'),
                'o':self.__channel__('output')
            }
        except:
            raise
        return self.__channels

    def __input_on_msg__(self,channel,method,properties,body):
        try:
            assert properties.headers['response']
            assert properties.headers['response-etag'] in self.tasks
        except (AssertionError,AttributeError,KeyError):
            self.log.info('no valid response')
        except:
            raise
        else:
            self.log.info('%s reply at %s' % (properties.headers['response-etag'],self.datetime_f))
            
            def on_decode(_):
                self.tasks[properties.headers['response-etag']](_.result())
                return True
            
            self.utcode.decode(body,future=self.ioengine.future(on_decode))

        ack(channel,method)(True)
        return True
    
    def request(self,future,body,exchange,rk=''):
        etag = self.etag
        self.tasks[etag] = future.set_result

        def on_encode(_):
            self.ch['output'].basic_publish(
                body=_.result(),
                exchange=exchange,
                properties=BasicProperties(headers={
                    'request':True,
                    'request-datetime':self.datetime_f,
                    'request-etag':etag,
                    'request-reply-exchange':self.__settings['exchange']['topic'],
                    'request-reply-rk':self.__settings['services']['input']['queue']
                }),
                routing_key=rk
            )
            self.log.info('%s requested at %s' % (etag,self.datetime_f))
            return True
        
        self.utcode.encode(body,future=self.ioengine.future(on_encode))
        return True
