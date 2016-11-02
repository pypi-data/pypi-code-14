from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import json


@Request.application
def application(request):
    data = request.get_data()
    data = json.loads(data.decode())

    method = data['method']

    response = {}

    if method == 'sayHello':
        response['jsonrpc'] = '2.0'
        response['result'] = 'Hello ' + data['params']['name']
        response['id'] = data['id']
        return Response(json.dumps(response) + '\n')
    elif method == 'notifyServer':
        print('server was notified')
        return Response()



def main():
    run_simple('localhost', 4000, application)


if __name__ == '__main__':
    main()
