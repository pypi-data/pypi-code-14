from rask.base import Base
from rask.options import define,options,parse_command_line
from tornado.web import Application

__all__ = ['Main']

class Main(Base):
    __http__ = None
    __http_routes__ = []
    __options__ = {
        'rmq':{
            'channel':{
                'prefetch':10
            }
        }
    }
    
    def __init__(self):
        self.before()
        self.setup()
        self.ioengine.loop.add_callback(self.after)
        self.ioengine.loop.add_callback(self.http)
        self.ioengine.start()

    def after(self):
        pass
        
    def before(self):
        pass

    def http(self):
        try:
            assert self.__http_routes__
        except AssertionError:
            return False
        except:
            raise
        else:
            self.__http__ = Application(self.__http_routes__,autoreload=options.autoreload)
            self.ioengine.loop.add_callback(
                self.__http__.listen,
                port=options.http_port,
                xheaders=True
            )
            self.log.info('HTTP Server - %s' % options.http_port)
        return True
    
    def setup(self):
        define('autoreload',default=False)
        define('http_port',default=8088)
        define('rask',default=self.__options__)
        parse_command_line()
        return True
