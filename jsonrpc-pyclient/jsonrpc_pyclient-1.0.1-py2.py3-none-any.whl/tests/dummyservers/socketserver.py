import socket
import json

class TcpSocketServer(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self, q):
        # create server socket
        self.s.bind(('127.0.0.1', 1238))
        self.s.listen(1)

        # pass True to client process so it knows
        # that we're ready
        q.put(True)
        conn, addr = self.s.accept()

        # wait for incoming data, then put it into a json object
        received = json.loads(conn.recv(1024).decode())

        if isinstance(received, list):
            responses = []
            for request in received:
                response = process_request(request)
                if response:
                    responses.append(response)
            conn.send((json.dumps(responses) + '\n').encode())
        else:
            response = process_request(received)
            if response:
                conn.send((json.dumps(response) + '\n').encode())

    def stop(self):
        self.s.close()

def process_request(request):
        method = request['method']
        if method == 'sayHello':
            response = {}
            response['jsonrpc'] = '2.0'
            response['result'] = 'Hello ' + request['params']['name']
            response['id'] = request['id']
        elif method == 'notifyServer':
            print('server was notified')
            response = None

        return response



if __name__ == '__main__':
    tcpsocketserver = TcpSocketServer()
    tcpsocketserver.run()
    tcpsocketserver.stop()
