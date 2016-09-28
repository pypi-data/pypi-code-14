from bottle import Bottle, response


"""
    Micro Bottle.py OOP REST library

    Support auto "OPTIONS" method and gevent
    ---
    Author: Jack Stdin <hellotan@live.ru>
"""

HTTP_METHODS = ["get", "post", "put", "patch", "options", "delete"]


class Route(object):
    def __init__(self, route):
        if isinstance(route, list):
            self.route_paths = route
        else:
            self.route_paths = [route]

    def __call__(self, obj):
        for route_path in self.route_paths:
            allowed_methods = set()

            for meth_name, meth_pointer in obj.__dict__.items():
                if meth_name.lower() in HTTP_METHODS:
                    route_callback = lambda mp=meth_pointer, *args, **kwargs: mp(obj, *args, **kwargs)
                    app.route(route_path, method=meth_name.upper())(route_callback)
                    allowed_methods.add(meth_name.upper())

            # If no user defined method for "OPTIONS",
            # create default
            if 'OPTIONS' not in allowed_methods:
                allowed_methods.add('OPTIONS', )
                app.route(route_path, method='OPTIONS', callback=lambda *args, **kwargs: (
                    response.add_header("Access-Control-Allow-Methods", ', '.join(allowed_methods)),
                    response.add_header("Access-Control-Allow-Origin", "*"),
                    response.add_header("Access-Control-Allow-Headers",
                                        "x-requested-with, content-type, accept, origin, authorization, x-csrftoken, user-agent, accept-encoding")
                ))
        return obj


class Error(object):
    def __init__(self, error_codes):
        if isinstance(error_codes, list):
            self.error_codes = error_codes
        else:
            self.error_codes = [error_codes]

    def __call__(self, obj):
        for error_code in self.error_codes:
            app.error_handler[error_code] = obj


app = Bottle()
