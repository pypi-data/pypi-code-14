import httplib
import json
import urlparse
import uuid

import pytest
from pytest_localserver.http import WSGIServer
from werkzeug import Request
from werkzeug import Response


class FestungApp(WSGIServer):
    def __init__(self, *args, **kwargs):
        kwargs.update(application=self)
        super(FestungApp, self).__init__(*args, **kwargs)

        self.queries = []
        self.responses = []

    @Request.application
    def __call__(self, request):
        try:
            status, content = self.responses[len(self.queries)]
        except IndexError:
            response = Response("No prepared response")
            response.status_code = httplib.NOT_IMPLEMENTED
            return response

        self.queries.append(request)

        response = Response(json.dumps(content))
        response.status_code = status
        response.headers['content-type'] = 'application/json'

        return response

    def add_response(self, data, status=httplib.OK):
        self.responses.append((status, data))

    @property
    def json_queries(self):
        return [json.loads(q.data) for q in self.queries]


@pytest.fixture
def festung():
    server = FestungApp()
    server.start()
    try:
        yield server
    finally:
        server.stop()


@pytest.fixture
def festung_url(festung):
    return festung.url


@pytest.fixture
def database():
    return uuid.uuid4().hex


@pytest.fixture
def database_url(festung_url, database):
    return urlparse.urljoin(festung_url, database)
