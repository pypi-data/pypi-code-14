from bottle import Bottle
from bottle import response

"""
    Micro Bottle.py OOP REST library
    ---
    Author: Jack Stdin <hellotan@live.ru>
    Usage example:

    from borest import BoRest

    class App(BoRest):
        def __init__(self):
            super(App, self).__init__()

        @BoRest.view('/hello/<username>')
        class Hello:
            @staticmethod
            def get(username):
                return "HELLO "+username

            @staticmethod
            def post(username):
                return "You cannot POST hello "+username
"""


class BoRest(object):
    view_methods = ('get', 'post', 'patch',)

    def __init__(self):
        self._app = Bottle()
        self.__init_routes()

    def __init_routes(self):
        for kw in dir(self):
            view = getattr(self, kw)
            if hasattr(view, 'is_route'):
                allowed_methods = set()
                allowed_methods.add('OPTIONS')
                for view_method in dir(view):
                    if view_method in self.view_methods:
                        method_f = getattr(view, view_method)
                        self._app.route(view.brest_route, method=view_method.upper(), callback=method_f)

                        allowed_methods.add(view_method.upper())
                self._app.route(view.brest_route, method='OPTIONS',
                                callback=lambda *x, **xx: response.add_header('Access-Control-Allow-Methods',
                                                                              ', '.join(allowed_methods)))
            elif hasattr(view, 'is_error'):
                self._app.error_handler[view.brest_error] = view

    def get_app(self):
        return self._app

    def start(self, **kwargs):
        self._app.run(**kwargs)

    # Route decorator
    @staticmethod
    def view(route):
        def decorator(f):
            f.is_route = True
            f.brest_route = route
            return f

        return decorator

    # Error decorator
    @staticmethod
    def error(error_code):
        def decorator(f):
            f.is_error = True
            f.brest_error = error_code
            return f

        return decorator
