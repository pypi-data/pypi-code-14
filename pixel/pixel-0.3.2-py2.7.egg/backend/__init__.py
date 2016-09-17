from __future__ import print_function

import os
import tornado.ioloop
import tornado.web as web
import webbrowser
import SocketServer

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('../frontend/index.html')

handlers = [
  (r'/frontend/(.*)', web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), '../../frontend/')}),
  (r'/', MainHandler)
]

settings = {'debug':True,}
application = web.Application(handlers, **settings)

def start_server():
    port = 8000
    while True:
      try:
          application.listen(port)
      except SocketServer.socket.error as exc:
          port += 1
      else:
          break
    print('Serving on port', port)
    webbrowser.open('http://localhost:{}'.format(port))
    tornado.ioloop.IOLoop.instance().start()