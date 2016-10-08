# coding: utf-8

import logging

from django.conf import settings
from django.test.client import RequestFactory
from typeddict import fields as f
from typeddict import TypedDict

from dj_tiny_api.v2 import BaseResult, Endpoint, logger


myhandler = logging.StreamHandler()  # writes to stderr
myformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
myhandler.setFormatter(myformatter)
logger.addHandler(myhandler)

settings.configure()
rf = RequestFactory()


class Args(TypedDict):
    a = f.String()


class Result(TypedDict):
    b = f.String()


@Endpoint(data_spec=Args, result_spec=Result)
def view(data, request):
    if data.a == "empty":
        return
    elif data.a == "invalid":
        return Result()
    return Result(b="")


def test_validation_error():
    request = rf.get("", HTTP_ACCEPT="application/json")
    response = view(request)
    assert response.status_code == 500
    assert response.content == b'{"error":{"code":"api:validation"}}'


def test_empty_response():
    request = rf.get("", data={"a": "empty"}, HTTP_ACCEPT="application/json")
    response = view(request)
    assert response.status_code == 200
    assert response.content == b'{}'


def test_ok():
    request = rf.get("", data={"a": ""}, HTTP_ACCEPT="application/json")
    response = view(request)
    assert response.status_code == 200
    assert response.content == b'{"data":{"b":""}}'


def test_unknown_error():
    request = rf.get("", data={"a": "invalid"}, HTTP_ACCEPT="application/json")
    response = view(request)
    assert response.status_code == 500
    assert response.content == b'{"error":{"code":"api:unknown"}}'


def test_unknown_accept():
    request = rf.get("", HTTP_ACCEPT="huyemoye")
    response = view(request)
    assert response.status_code == 500
    assert response.content == b'{"error":{"code":"api:unknown_accept"}}'
