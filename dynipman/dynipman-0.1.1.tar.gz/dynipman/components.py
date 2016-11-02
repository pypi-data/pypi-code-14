import os, json, datetime, time, socket, requests
from distutils import file_util
from importlib.machinery import SourceFileLoader
from dynipman.crypto import randkey, sencrypt, sdecrypt, make_keypair, load_keypair, encrypt, decrypt, sign, verify

# _base_dir = os.path.join(os.path.expanduser('~'), '.dynipman') #running with current user
_base_dir = os.path.join('/var/lib/', 'dynipman') #running under root - for Upstart init

class ClientKeyNotFound(Exception):
    pass

class TempKeyExpired(Exception):
    pass

def load_config():
    if not os.path.exists(_base_dir):
        os.makedirs(_base_dir)
    if not os.path.exists(os.path.join(_base_dir, 'conf')):
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.py')
        file_util.copy_file(config_file, os.path.join(_base_dir, 'conf'))
    confpy = SourceFileLoader('conf', os.path.join(_base_dir, 'conf')).load_module()
    return confpy

class Server():
    def __init__(self):
        config = load_config()
        
        self.config = config.SERVER
        self.key = config.SHARED_KEY
        self.addressbook = self.load_addressbook()
        
        self.use_RSA = config.USE_RSA
        self.keypair = None
        self.client_pubkeys = {}
        self.client_tempkeys = {}
        if self.use_RSA:
            self.load_rsa_keys()
            
    def authenticate(self, handler):
#         print(handler.request.body)
        if self.use_RSA:
            client = handler.get_query_arguments('client')[0]
            if not client in self.client_tempkeys.keys():
                raise TempKeyExpired
            post_data = json.loads(sdecrypt(self.client_tempkeys[client], handler.request.body))
            message = post_data[0]
            signature = (post_data[1][0], )
#             print(message)
#             print(signature)
            try:
                authorized = verify( self.client_pubkeys[client], message, signature )
                return authorized
            except KeyError:
                raise ClientKeyNotFound
        else:
            post_data = json.loads(sdecrypt(self.key, handler.request.body))
            code = [post_data['code']]
            if len(code) > 0:
                return (code[0] == self.key)
            else:
                return False
    
    def load_addressbook(self):
        result = {}
        try:
            with open(os.path.join(_base_dir, self.config['data_file']), 'r') as bookfile:
                result = json.loads(bookfile.read())
        except ValueError:
            pass
        finally:
            return result
        
    def save_addressbook(self):
        try:
            with open(os.path.join(_base_dir, self.config['data_file']), 'w') as bookfile:
                data = json.dumps(self.addressbook)
                bookfile.write(data)
            return True
        except ValueError:
            return False
        
    def load_rsa_keys(self):
        try:
            self.keypair = load_keypair('server.private', _base_dir)
            print("Successfully loaded RSA keys for the Server")
        except FileNotFoundError:
            print("Could not find RSA keypair, generating a new keypair for the Server")
            self.keypair = make_keypair('server', _base_dir)
        
        client_keypath = os.path.join(_base_dir, 'client_keys')
        if not os.path.exists(client_keypath):
            os.makedirs(client_keypath)
        filelist = os.listdir(client_keypath)
        for file in filelist:
            if os.path.isfile(os.path.join(client_keypath, file)):
                client_name = os.path.splitext(file)[0]
                self.client_pubkeys[client_name] = load_keypair(file, client_keypath)
                print("    Found RSA public key for "+client_name)
        
    def make_tempkey(self, request):
        if self.use_RSA:
            post_data = json.loads(request.body.decode())
            tempkey = randkey()
            self.client_tempkeys[post_data['name']] = tempkey
            try:
                encrypted_key = encrypt(self.client_pubkeys[post_data['name']], tempkey)
                return encrypted_key
            except KeyError:
                print(" Could not find public key for ["+post_data['name']+"]")
                return self.key
        else:
            return self.key
            
        
    def update_address(self, name, new_info):
        self.addressbook[name] = new_info
        result = self.save_addressbook()
        if result:
            with open(os.path.join(_base_dir, 'log.txt'), 'a') as logfile:
                new_info['dtstamp'] = datetime.datetime.utcnow().isoformat()
                data = json.dumps(new_info)+'\n'
                logfile.write(data)
        return result
    
    def update(self, handler):
        if self.use_RSA:
            client = handler.get_query_arguments('client')[0]
            if not client in self.client_tempkeys.keys():
                raise TempKeyExpired
            post_data = json.loads(sdecrypt(self.client_tempkeys[client], handler.request.body))
            message = json.loads(post_data[0])
            client_info = {
                           'ip': handler.request.remote_ip,
                           'host': message['host'],
                           'name': message['name'],
                           }
            encryption_key = self.client_tempkeys[client]
        else:
            post_data = json.loads(sdecrypt(self.key, handler.request.body))
            client_info = {
                           'ip': handler.request.remote_ip,
                           'host': post_data['host'],
                           'name': post_data['name'],
                           }
            encryption_key = self.key
        print(datetime.datetime.utcnow())
        print("IP Update Request from "+client_info['name'])
        print('    Client host : '+client_info['host'])
        print('    Client IP   : '+client_info['ip'])
        saved = self.update_address(client_info['name'], client_info)
        if saved:
            response = { 'result': 'success', 'data': 'Update saved successfully', }
        else:
            response = { 'result': 'failure', 'data': 'Failed to save data', }
        return sencrypt(encryption_key, json.dumps(response))


class Client():
    def __init__(self):
        self.config = load_config()
        self.info = {
                     'host': socket.gethostname(),
                     'name': self.config.CLIENT['name']
                     }
        self.key = self.config.SHARED_KEY
        
        self.keypair = None
        self.server_pubkey = None
        if self.config.USE_RSA:
            self.load_rsa_keys()
    
    def load_rsa_keys(self):
        try:
            self.keypair = load_keypair(self.info['name']+'.private', _base_dir)
            print("Successfully loaded RSA keys for ["+self.info['name']+"]")
        except FileNotFoundError:
            print("Could not find RSA keypair, generating a new keypair for ["+self.info['name']+"]")
            self.keypair = make_keypair(self.info['name'], _base_dir)
        
        try:
            self.server_pubkey = load_keypair('server.public', _base_dir)
            print("Successfully loaded Server Public Key")
        except FileNotFoundError:
            raise FileNotFoundError("Could not find Server RSA Public Key. Please obtain a copy and save it in "+_base_dir)
        self.key = None
        
    def report_ip(self):
        try:
            post_data = self.info.copy()
            post_data['code'] = self.key
            response = requests.post(self.config.SERVER['url']+'update/', data=sencrypt(self.key, json.dumps(post_data))).content
            update = json.loads(sdecrypt(self.key, response))
            print(datetime.datetime.now())
#             print(response)
            print(update)
            return update
        except requests.exceptions.ConnectionError:
            print(datetime.datetime.now())
            print('Connection Error!')
            print('  check config at '+os.path.join(_base_dir, 'conf'))
            print('  if the config is correct, then the server might be down.')
            return None
        
    def report_ip_rsa(self):
        try:
            if not self.key:
                try:
                    self.key = self.get_tempkey()
                except UnicodeDecodeError:
                    print("!!!Could not decrypt response from server. \nMake sure that this client's public key is copied into "+os.path.join(_base_dir, 'client_keys')+" on the server")
                    return None
#                 print(self.key)
            post_data = self.info.copy()
            post_data['randkey'] = randkey() #random key just to change signature every request
            message = json.dumps(post_data)
            signature = sign(self.keypair, message)
            ciphertext = sencrypt(self.key, json.dumps([message, signature]))
#             print(message)
#             print(signature)
#             print(ciphertext)
            response = requests.post(self.config.SERVER['url']+'update/?client='+self.info['name'], data=ciphertext)
            try:
                update = json.loads(sdecrypt(self.key, response.content))
                print(datetime.datetime.now())
                print(update)
                return update
            except ValueError:
                resp_data = response.json()
                print(resp_data)
                if 'error' in resp_data.keys():
                    if resp_data['error'] == "TempKeyExpired":
                        self.key = None
                    elif resp_data['error'] == "ClientKeyNotFound":
                        print("This client's public key is not registered with the server.\nPlease copy the public key to the server.")
                return None
        except requests.exceptions.ConnectionError:
            print(datetime.datetime.now())
            print('Connection Error!')
            print('  check config at '+os.path.join(_base_dir, 'conf'))
            print('  if the config is correct, then the server might be down.')
            return None
        
    def get_tempkey(self):
        if self.config.USE_RSA:
            try:
                response = requests.post(self.config.SERVER['url']+'tempkey/', data=json.dumps({'name': self.info['name']}))
                tempkey = decrypt(self.keypair, response.content)
                return tempkey
            except requests.exceptions.ConnectionError:
                print(datetime.datetime.now())
                print('Connection Error!')
                print('  check config at '+os.path.join(_base_dir, 'conf'))
                print('  if the config is correct, then the server might be down.')
                return None
    
    def start(self):
        while True:
            if self.config.USE_RSA:
                self.report_ip_rsa()
            else:
                self.report_ip()
            time.sleep(self.config.CLIENT['update_interval'])