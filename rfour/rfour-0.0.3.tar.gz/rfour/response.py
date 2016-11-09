from common import datetime_f
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import BasicProperties

__all__ = ['Response']

class Response(Base):
    @property
    def datetime_f(self):
        return datetime_f()
    
    @property
    def utcode(self):
        try:
            assert self.__utcode
        except (AssertionError,AttributeError):
            self.__utcode = UTCode()
        except:
            raise
        return self.__utcode

    def push(self,body,headers,channel):
        def on_push(_):
            try:
                assert _.result()
            except:
                raise
            else:
                channel.basic_publish(**_.result())
            return True
        
        self.ioengine.loop.add_callback(
            self.response,
            body=body,
            headers=headers,
            future=self.ioengine.future(on_push)
        )
        return True
    
    def response(self,body,headers,future):
        try:
            assert headers['rfour']
            assert headers['request']
            assert headers['request-etag']
            assert headers['request-reply-exchange']
            assert headers['request-reply-rk']
        except (AssertionError,KeyError):
            future.set_result(False)
            return False
        except:
            raise
                    
        def on_encode(_):
            future.set_result({
                'body':_.result(),
                'exchange':headers['request-reply-exchange'],
                'properties':BasicProperties(headers={
                    'rfour':True,
                    'response':True,
                    'response-datetime':self.datetime_f,
                    'response-etag':headers['request-etag']
                }),
                'routing_key':headers['request-reply-rk']
            })
            return True
        
        self.utcode.encode(body,future=self.ioengine.future(on_encode))
        return True
