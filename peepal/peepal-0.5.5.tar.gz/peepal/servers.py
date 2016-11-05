import os

def run_wsgiref(app, host, port, **kwargs):
    from wsgiref.simple_server import make_server, WSGIRequestHandler
    
    class QuietHandler(WSGIRequestHandler):
        def log_request(*args, **kw): 
            pass

    server = make_server(host, port, app, handler_class=QuietHandler)
    server.serve_forever()

def run_cherrypy(app, **kwargs):
    from cherrypy.wsgiserver import CherryPyWSGIServer

    max_request_header_size = kwargs.pop('max_request_header_size', 1024 * 8)
    max_request_body_size = kwargs.pop('max_request_body_size', 1024 * 1024 * 4)

    options = {
            'numthreads': 15, # thread pool min threads.
            'max': 15, # thread pool max threads.
            'timeout': 3, # socket timeout, in seconds. 
            'request_queue_size': 16, # The 'backlog' arg to socket.listen(); default: 5
    }
    options.update(wsgi_app=app, **kwargs)
    assert options['max'] >= options['numthreads']

    server = CherryPyWSGIServer(**options)

    server.max_request_header_size = max_request_header_size
    server.max_request_body_size = max_request_body_size
    server.start()

def run(app, server='wsgiref', *, autoreload=False, quiet=True, **kwargs):
    if not quiet:
        if not autoreload or os.environ.get('RUN_MAIN') == 'true':
            print("Server starting up (using %s)..." % server)
            if 'host' in kwargs and 'port' in kwargs:
                print("Listening on http://%s:%d/" % (kwargs['host'], kwargs['port']))
            print("Use Ctrl-C to quit.")
            print()
        else:
            print("autoreload starting up...")

    func = globals()['run_' + server]
    try:
        if autoreload:
            from .autoreload import main
            main(lambda: func(app, **kwargs))
        else:
            func(app, **kwargs)
    except KeyboardInterrupt:
        if not quiet: 
            print("Shutting Down...")

