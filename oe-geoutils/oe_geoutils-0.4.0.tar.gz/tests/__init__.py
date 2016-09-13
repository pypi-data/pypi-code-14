# -*- coding: utf-8 -*-
import sys
import responses
import re
import json
import os


def text_(s, encoding='latin-1', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    # True if we are running on Python 3.
    PY3 = sys.version_info[0] == 3
    if PY3:
        binary_type = bytes
    else:
        binary_type = str
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s

with open(os.path.join(os.path.dirname(__file__), 'fixtures/get_gemeente_results.json'), 'rb') as f:
    get_gemeente_results = json.loads(text_(f.read()))
with open(os.path.join(os.path.dirname(__file__), 'fixtures/get_provincie_results.json'), 'rb') as f:
    get_provincie_results = json.loads(text_(f.read()))


def mock_geozoekdiensten_response(base_url='http://geozoekdienst.en', response_status=200):
    def callback(request):
        resp_body = [{'naam': 'gemeente'}]
        headers = {'content_type': 'application/json'}
        return response_status, headers, json.dumps(resp_body)

    responses.add_callback(
        responses.POST,
        re.compile(r'^({0}).+'.format(base_url)),
        callback=callback)
    return base_url


def mock_geozoekdiensten_get_gemeente_response(len_results, base_url='http://geozoekdienst.en'):
    def callback(request):
        if len_results == 2:
            resp_body = get_gemeente_results
        elif len_results == 1:
            resp_body = [{'naam': 'gemeente', 'id': 'niscode'}]
        else:
            resp_body = []
        headers = {'content_type': 'application/json'}
        return 200, headers, json.dumps(resp_body)

    responses.add_callback(
        responses.POST,
        re.compile(r'^({0}).+'.format(base_url)),
        callback=callback)
    return base_url
