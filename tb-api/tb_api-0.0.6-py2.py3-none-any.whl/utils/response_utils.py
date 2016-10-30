# encoding=utf-8
import json

from flask import Response


def build_error_response(data):
    content = json.dumps(data)
    mimetype = 'application/json'
    return Response(content, status=404,
                    mimetype=mimetype)


def error_response(content):
    return Response(content, status=404)
