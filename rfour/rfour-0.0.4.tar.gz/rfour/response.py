from common import datetime_f
from rask.base import Base
from rask.parser.utcode import UTCode
from rask.rmq import BasicProperties

__all__ = ['Response']

class Response(Base):
    @property
    def datetime(self):
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

    def __response_body(self,body,future):
        def on_encode(_):
            future.set_result(_.result())
            return True
        
        self.utcode.encode(body,future=self.ioengine.future(on_encode))
        return True

    def __response_headers(self,headers,future,result=None,_=None):
        try:
            k = _.next()
            assert not k.startswith('request')
        except AssertionError:
            self.ioengine.loop.add_callback(
                self.__response_headers,
                headers=headers,
                future=future,
                result=result,
                _=_
            )
        except AttributeError:
            headers.update({
                'rfour':True,
                'response':True,
                'response-datetime':self.datetime,
                'response-etag':headers['request-etag']
            })
                        
            self.ioengine.loop.add_callback(
                self.__response_headers,
                headers=headers,
                future=future,
                result={},
                _=iter(headers)
            )
        except StopIteration:
            future.set_result(BasicProperties(headers=result))
            return True
        except:
            raise
        else:
            result[k] = headers[k]
            
            self.ioengine.loop.add_callback(
                self.__response_headers,
                headers=headers,
                future=future,
                result=result,
                _=_
            )
        return None
    
    def push(self,body,headers,channel):
        def on_push(_):
            try:
                assert _.result()
            except:
                raise
            else:
                channel.basic_publish(
                    exchange=headers['request-reply-exchange'],
                    routing_key=headers['request-reply-rk'],
                    **_.result()
                )
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
            self.validate_headers(headers)
        except (AssertionError,KeyError):
            future.set_result(False)
            return False
        except:
            raise
        else:
            def on_headers(p):
                def on_body(b):
                    future.set_result({
                        'body':b.result(),
                        'properties':p.result()
                    })
                    return True
                
                self.ioengine.loop.add_callback(
                    self.__response_body,
                    body=body,
                    future=self.ioengine.future(on_body)
                )
                return True
            
            self.ioengine.loop.add_callback(
                self.__response_headers,
                headers=headers,
                future=self.ioengine.future(on_headers)
            )
        return True                   

    def validate_headers(self,headers):
        try:
            assert headers['rfour']
            assert headers['request']
            assert headers['request-etag']
            assert headers['request-reply-exchange']
            assert headers['request-reply-rk']
        except:
            raise
        return True
