import os
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed

def find_key(token):
    if os.environ.get('ACME_TOKEN') == token:
        return os.environ.get('ACME_KEY')
    for k, v in os.environ.items():
        if v == token and k.startswith('ACME_TOKEN_'):
            n = k.replace("ACME_TOKEN_", "")
            return os.environ.get("ACME_KEY_{}".format(n))
    return None

def acme_challenge(request, acme_token):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    key = find_key(acme_token)
    if key is None:
        return HttpResponseNotFound()
    return HttpResponse(key, content_type="text/plain")
