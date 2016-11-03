from gwebsocket.handler import WebSocketHandler
from gunicorn.workers.ggevent import GeventPyWSGIWorker


class GWebSocketWorker(GeventPyWSGIWorker):
    wsgi_handler = WebSocketHandler
