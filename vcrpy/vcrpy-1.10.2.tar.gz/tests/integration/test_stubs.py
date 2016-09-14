import vcr
import zlib
import six.moves.http_client as httplib

from assertions import assert_is_json


def _headers_are_case_insensitive(host, port):
    conn = httplib.HTTPConnection(host, port)
    conn.request('GET', "/cookies/set?k1=v1")
    r1 = conn.getresponse()
    cookie_data1 = r1.getheader('set-cookie')
    conn = httplib.HTTPConnection(host, port)
    conn.request('GET', "/cookies/set?k1=v1")
    r2 = conn.getresponse()
    cookie_data2 = r2.getheader('Set-Cookie')
    return cookie_data1 == cookie_data2


def test_case_insensitivity(tmpdir, httpbin):
    testfile = str(tmpdir.join('case_insensitivity.yml'))
    # check if headers are case insensitive outside of vcrpy
    host, port = httpbin.host, httpbin.port
    outside = _headers_are_case_insensitive(host, port)
    with vcr.use_cassette(testfile):
        # check if headers are case insensitive inside of vcrpy
        inside = _headers_are_case_insensitive(host, port)
        # check if headers are case insensitive after vcrpy deserializes headers
        inside2 = _headers_are_case_insensitive(host, port)

    # behavior should be the same both inside and outside
    assert outside == inside == inside2


def _multiple_header_value(httpbin):
    conn = httplib.HTTPConnection(httpbin.host, httpbin.port)
    conn.request('GET', "/response-headers?foo=bar&foo=baz")
    r = conn.getresponse()
    return r.getheader('foo')


def test_multiple_headers(tmpdir, httpbin):
    testfile = str(tmpdir.join('multiple_headers.yaml'))
    outside = _multiple_header_value(httpbin)

    with vcr.use_cassette(testfile):
        inside = _multiple_header_value(httpbin)

    assert outside == inside


def test_original_decoded_response_is_not_modified(tmpdir, httpbin):
    testfile = str(tmpdir.join('decoded_response.yml'))
    host, port = httpbin.host, httpbin.port

    conn = httplib.HTTPConnection(host, port)
    conn.request('GET', '/gzip')
    outside = conn.getresponse()

    with vcr.use_cassette(testfile, decode_compressed_response=True):
        conn = httplib.HTTPConnection(host, port)
        conn.request('GET', '/gzip')
        inside = conn.getresponse()

        # Assert that we do not modify the original response while appending
        # to the casssette.
        assert 'gzip' == inside.headers['content-encoding']

        # They should effectively be the same response.
        inside_headers = (h for h in inside.headers.items() if h[0].lower() != 'date')
        outside_headers = (h for h in outside.getheaders() if h[0].lower() != 'date')
        assert set(inside_headers) == set(outside_headers)
        inside = zlib.decompress(inside.read(), 16+zlib.MAX_WBITS)
        outside = zlib.decompress(outside.read(), 16+zlib.MAX_WBITS)
        assert inside == outside

    # Even though the above are raw bytes, the JSON data should have been
    # decoded and saved to the cassette.
    with vcr.use_cassette(testfile):
        conn = httplib.HTTPConnection(host, port)
        conn.request('GET', '/gzip')
        inside = conn.getresponse()

        assert 'content-encoding' not in inside.headers
        assert_is_json(inside.read())
