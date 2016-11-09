from functools import partial

class Router(object):
    def __init__(self):
        self.routings = []
        self.path_stack = ""
        self.ware_stack = []

    def __new__(cls, *args, **kwargs):  
        if not hasattr(cls, '_instance'):  
            orig = super(Router, cls)  
            cls._instance = orig.__new__(cls, *args, **kwargs)  
        return cls._instance

    @classmethod
    def instance(cls, *args, **kwargs):
        return cls.__new__(cls, *args, **kwargs)      

    def _register(self, path, handler, middlewares):

        def _register_func(self, path, handler, middlewares):
            original_path = self.path_stack
            original_ware = self.ware_stack.copy()

            self.path_stack += path
            self.ware_stack.extend(middlewares)

            middleware_dict = {"middlewares": self.ware_stack}
            routing = (self.path_stack, handler, middleware_dict)
            # 格式(r"/", MainHandler,{"middlewares":[Middleware1, Middleware2]})
            self.routings.append(routing)

            self.path_stack = original_path
            self.ware_stack = original_ware

        return partial(_register_func, self, path, handler, middlewares)

    
    def _group(self, path, middlewares, callbacks):
        def _group_func(self, path, middlewares, callbacks):    
            original_path = self.path_stack
            original_ware = self.ware_stack.copy()

            self.path_stack += path
            self.ware_stack.extend(middlewares)

            for call in callbacks: call()

            self.path_stack = original_path
            self.ware_stack = original_ware
        return partial(_group_func, self, path, middlewares, callbacks)

    def _represent(self):
        for r in self.routings:
            print(r)

# method utils 
def group(*args, **kwargs):
    return Router.instance()._group(*args, **kwargs)

def _method(*args, **kwargs):
	return Router.instance()._register(*args, **kwargs)

GET=PATCH=POST=PUT=DELETE=OPTIONS=_method




if __name__ == '__main__':
    r = Router()
    group("/-a", ["-1", "-2"],
        (
            GET("/-b", "-p", ["-3", "-4"]),
            PUT("/-c", "-l", ["-5"]),

            group("/-d",["-6", "-7"],
                (
                    OPTIONS("/-e", "-m", ["-8", "-9"]),
                    DELETE("/-f", "-k", ["-10"]),
                    )
                )
            )
        )()
    
    GET("/b", "p", ["3", "4"])()
    group("/a", ["1", "2"],
        (
            GET("/b", "p", ["3", "4"]),
            PUT("/c", "l", ["5"]),

            group("/d",["6", "7"],
                (
                    OPTIONS("/e", "m", ["8", "9"]),
                    DELETE("/f", "k", ["10"]),
                    )
                )
            )
        )()

    r._represent()