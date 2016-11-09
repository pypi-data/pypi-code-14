import tornado.ioloop
import tornado.web

class MiddleHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        self.middlewares = kwargs["middlewares"]

    def prepare(self):
        for ware in self.middlewares:
            if "before_process" in ware.__dict__:
                ware.before_process(self)

    def on_finish(self):
        # on_finish 是在输出完了以后，做什么也改不了输出了
        # 大概用来clean up, 或者logging
        for ware in self.middlewares:
            if "after_process" in ware.__dict__:
                ware.after_process(self)



if __name__ == "__main__":
    from tornado.web import Finish

    class Middleware1(object):
        @staticmethod
        def before_process(handler):
            handler.write(str(handler.request.arguments)+"\nraise Finish()")
            # 返回啥都没用，要不然就raise Finish()
            raise Finish()

    class Middleware2(object):
        @staticmethod
        def after_process(handler):
            print("after_process")



    class MainHandler(FlowHandler):
        def get(self):
            pass
        
    def make_app():
        return tornado.web.Application([
            (r"/", MainHandler,{"middlewares":[Middleware1, Middleware2]}),
        ])


    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
