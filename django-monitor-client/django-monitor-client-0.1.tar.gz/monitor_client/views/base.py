import json
import socket
from urllib import request

from django.http import HttpResponse
from django.conf import settings


def health_check(request):
    msg = {"version": "v1",
           "status": "ok",
           "code": "0x0001"}
    response_msg = json.dumps(msg)
    return HttpResponse(response_msg)


def register_app():
    send_url = settings.MONITOR_SERVER_PUSH_URL

    hostname = socket.gethostname()
    domain = settings.PROJIECT_DOMAIN
    secret_key = settings.SECRET_KEY
    project_name = settings.ROOT_URLCONF.split('.')[0]

    msg = {"hostname": hostname,
           "domain": domain,
           "secret_key": secret_key,
           "project_name": project_name,
           }

    send_msg = json.dumps(msg).encode('utf-8')
    response = request.urlopen(url=send_url, data=send_msg)


if True:
    register_app()
