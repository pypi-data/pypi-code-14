import websocket, json, requests

class   RTM():
    def __init__(self, token):
        self.TOKEN = token
        self.connected = False
        self.session = requests.Session()
        self.ws = websocket.WebSocket()

    def receive_dict(self):
        return json.loads(self.ws.recv())


    def connect(self):
        self.json_response = self.session.get(
            'https://slack.com/api/rtm.start',
            params={
                'token': self.TOKEN,
                'simple_latest': 'true',
                'no_unreads': 'true'
            }).json()
        if self.json_response['ok']:
            self.socket_url = self.json_response['url']
            print('url received')
            self.ws.connect(self.socket_url)
            hello = self.receive_dict()
            if hello['type'] == 'hello':
                print('Successfully connected to socket')
                self.connected = True
                return True
            elif hello['type'] == 'error':
                print('Error connecting to the socket...')
                print('Error message:', hello['error']['msg'])
                retry = input('Retry?(Y/n)')
                if retry.lower() == 'y' or retry == '' or retry.lower() == 'yes':
                    return self.connect()
                else:
                    return False
        else:
            print('Error while getting the url:', self.json_response['error'])
            return False

    def msg(self, msg, channel="D0HJBJSG3"): #channel with therightman
        self.ws.send(json.dumps({
            "id": 1,
            "type": "message",
            "channel": channel,
            "text": msg
        }))
