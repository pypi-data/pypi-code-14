import os
import tornado.ioloop
import tornado.web as web
import webbrowser
import SocketServer

def create_app(tmpfolder):
  handlers = [
    (r'/images/(.*)', web.StaticFileHandler, 
      {'path': tmpfolder}),
    (r'/(.*)', web.StaticFileHandler, 
      {'path': os.path.join(os.path.dirname(__file__), '../frontend'),
       "default_filename": "index.html"}),
  ]
  settings = {'debug':False,}
  return web.Application(handlers, **settings)

def start_server(tmpfolder):
    port = 8000
    application = create_app(tmpfolder)
    while True:
      try:
          application.listen(port)
      except SocketServer.socket.error as exc:
          port += 1
      else:
          break
    print 'Serving on port', port
    webbrowser.open('http://localhost:{}'.format(port))
    tornado.ioloop.IOLoop.instance().start()