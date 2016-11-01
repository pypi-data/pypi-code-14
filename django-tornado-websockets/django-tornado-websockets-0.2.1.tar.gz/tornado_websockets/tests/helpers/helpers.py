from tornado import gen
from tornado.testing import AsyncHTTPTestCase
from tornado.websocket import websocket_connect

from tornado_websockets.websockethandler import WebSocketHandler

try:
    from tornado import speedups
except ImportError:
    speedups = None

