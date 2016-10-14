import mock
import requests
import six
from applause import utils


def test_get_emails():
    emails = [
        "test1@example.com",
        b"""
            test2@example.com 
                test3@example.com
    
    test4@example.com    
        """,
        "test5@example.com",
    ]
    assert utils.get_emails(emails) == [
        "test1@example.com",
        "test2@example.com",
        "test3@example.com",
        "test4@example.com",
        "test5@example.com",
    ]


def test_download():
    session = requests.Session()
    output = six.StringIO()

    response = requests.Response()
    response.status_code = 200
    response.iter_content = lambda *args, **kwargs: ['a', 'b', 'c']
    response.headers['content-length'] = 3

    with mock.patch.object(session, 'get') as get:
        get.return_value = response
        data = list(utils.download('http://test.zip', output, session=session, chunk_size=1))

    get.assert_called_once_with('http://test.zip', stream=True)
    # Download status, 1/3 -> 2/3 -> 3/3 -> Stop iteration
    assert data == [(1, 3), (2, 3), (3, 3)]
    assert output.getvalue() == 'abc'
