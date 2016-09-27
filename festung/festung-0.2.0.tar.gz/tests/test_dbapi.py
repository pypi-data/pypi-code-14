import base64
import datetime
import decimal

import pytest
import pytz

import festung.dbapi


@pytest.fixture
def connection(database_url):
    conn = festung.dbapi.Connection(database_url)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def cursor(connection):
    cur = connection.cursor()
    try:
        yield cur
    finally:
        cur.close()


class ResponseFixture(object):
    @pytest.fixture(autouse=True)
    def prepare_response(self, festung):
        festung.add_response(self.response)

    @property
    def data(self):
        return self.response['data']


class TestEmptyResponse(ResponseFixture):
    response = {'data': [], 'headers': []}

    def test_execute(self, festung, cursor):
        query = 'SELECT * FROM foo'
        params = ['string', 1, None]
        cursor.execute(query, params)

        [data] = festung.json_queries
        assert data['sql'] == query
        assert data['params'] == params

    @pytest.mark.parametrize('param,expected_serialialized', [
        (datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.UTC), '1970-01-01T00:00:00+00:00'),
        (datetime.date(1970, 1, 1), '1970-01-01'),
        (datetime.time(0, 0, 0), '00:00:00'),
        (decimal.Decimal('1234.5678'), '1234.5678'),
    ])
    def test_binding_cast(self, festung, cursor, param, expected_serialialized):
        cursor.execute('SELECT 1', [param])
        [data] = festung.json_queries
        [serialized] = data['params']

        assert serialized == expected_serialialized

    def test_password_is_sent(self, cursor, password, festung):
        cursor.execute('SELECT * FROM foo')
        [query] = festung.queries
        assert base64.b64decode(query.headers['Authorization']) == password


class TestDummyResponseWithExecutedCursor(ResponseFixture):
    response = {'data': [['a', 1], ['b', 2]], 'headers': ['bar', 'baz']}

    @pytest.fixture(autouse=True)
    def run_query(self, cursor):
        cursor.execute("SELECT * FROM foo")

    def test_fetchone(self, cursor):
        assert cursor.fetchone() == tuple(self.data[0])
        assert cursor.fetchone() == tuple(self.data[1])
        assert cursor.fetchone() is None

    def test_fetchall_same_size_than_response(self, cursor):
        cursor.arraysize = len(self.data)
        assert cursor.fetchmany() == [tuple(row) for row in self.data]

    def test_fetchall_smaller_size_than_response(self, cursor):
        cursor.arraysize = 1
        assert cursor.fetchmany() == [tuple(self.data[0])]

    def test_fetchall_bigger_size_than_response(self, cursor):
        cursor.arraysize = len(self.data) * 10
        assert cursor.fetchmany() == [tuple(row) for row in self.data]
