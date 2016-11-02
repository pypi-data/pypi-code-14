import json
from dynipman.components import Server, ClientKeyNotFound, TempKeyExpired
from dynipman.crypto import sencrypt
import tornado.ioloop
from tornado.web import Application, URLSpec, RequestHandler
    
running_server = Server()

def is_authorized(handler, server):
    if handler.request.method == 'GET':
        code = handler.get_query_arguments('code')
    elif handler.request.method == 'POST':
        post_data = json.loads(handler.request.body.decode())
        code = [post_data['code']]
    if len(code) > 0:
        return (code[0] == server.key)
    else:
        return False

class MainHandler(RequestHandler):
    def get(self):
        context = {
                   'test': 'TESTING'
                   }
        self.render('index.html', title='dynipman', context=context)
        
    def post(self):
        if is_authorized(self, running_server):
            message = json.dumps(running_server.addressbook)
            self.write(message)
            print("Main - Authorized")
        else:
            self.write("Unauthorized")
            print("Main - UNAUTHORIZED")
#         print(repr(self.request))
#         print(self.request.body)
        
class UpdateHandler(RequestHandler):
    def post(self):
        try:
            if running_server.authenticate(self):
                print('Update - Authorized')
                result = running_server.update(self)
                self.write( result )
            else:
                print('Update - UNAUTHORIZED')
                self.write( { 'result': 'failure', 'data': 'Unauthorized Access', } )
        except ClientKeyNotFound:
            self.write( { 'result': 'failure', 'data': 'Public Key Not Registered', 'error': "ClientKeyNotFound"} )
        except TempKeyExpired:
            self.write( { 'result': 'failure', 'data': "Temporary Key Expired", 'error': "TempKeyExpired" })
    #         print(repr(self.request))
    #         print(self.request.body)
        
        
class TempKeyHandler(RequestHandler):
    def post(self):
        tempkey = running_server.make_tempkey(self.request)
        self.write( tempkey )
        
def make_app():
    print('========================')
    print(' starting dynipman server ')
    print('    using RSA: '+str(running_server.use_RSA))
    print('========================')
    return Application([ URLSpec(r'/$', MainHandler, name='main'),
                         URLSpec(r'/update/$', UpdateHandler, name='update'),
                         URLSpec(r'/tempkey/$', TempKeyHandler, name='tempkey'), 
                        ])
    
def run():
    app = make_app()
    app.listen(running_server.config['port'])
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    run()