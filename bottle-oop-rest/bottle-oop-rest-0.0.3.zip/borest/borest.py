from bottle import Bottle, response

"""
    Micro Bottle.py OOP REST library
    ---
    Author: Jack Stdin <hellotan@live.ru>
"""

HTTP_METHODS = ["get", "post", "put", "patch", "options", "delete"]


class Route(object):
    def __init__(self, route):
        self.route_path = route

    def __call__(self, obj):
        allowed_methods = set()
        allowed_methods.add('OPTIONS', )

        for meth_name, meth_pointer in obj.__dict__.items():
            if meth_name.lower() in HTTP_METHODS:
                route_callback = lambda mp=meth_pointer, *args, **kwargs: mp(obj, *args, **kwargs)
                app.route(self.route_path, method=meth_name.upper())(route_callback)
                allowed_methods.add(meth_name.upper())

        app.route(self.route_path, method='OPTIONS', callback=lambda *args, **kwargs: (
            response.add_header("Access-Control-Allow-Methods", ', '.join(allowed_methods)),
            response.add_header("Access-Control-Allow-Origin", "*")
        ))
        return obj


class Error(object):
    def __init__(self, error):
        self.error_code = error

    def __call__(self, obj):
        app.error_handler[self.error_code] = obj


app = Bottle()
