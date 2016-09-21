import pytest

from timberjack.processors import CensorSensitiveDataProcessor


@pytest.mark.parametrize('uncensored,expected', [
    (
        'Nothing to see here',
        'Nothing to see here',
    ),
    (
        'MY_API_KEY=f00bar, asdfasdf',
        'MY_API_KEY=f0***** asdfasdf',
    ),
    (
        'MY_QUOTED_API_KEY="f00bar"',
        'MY_QUOTED_API_KEY="f0****"',
    ),
    (
        'MY_API_KEY=f00bar ANOTHER_KEY=12345',
        'MY_API_KEY=f0**** ANOTHER_KEY=12***',
    ),
    (
        'MY_API_TOKEN=JskaosUSb+Tjs=',
        'MY_API_TOKEN=Js************',
    ),
    (
        'MY_API_TOKEN="f00bar2000"',
        'MY_API_TOKEN="f0********"',
    ),
    (
        'url postgresql://user:password@host.com:12345/path',
        'url postgresql://user:pa******@host.com:12345/path',
    ),
    (
        'request_header=\'{"authorization": "Bearer JskaosUSb+Tjs="}\'',
        'request_header=\'{"authorization": "Bearer Js************"}\'',
    ),
    (
        """INFO 2016-05-19 12:57:18,191 base 3 140567301887808 event='api_client_make_request' request_id='fdad88dc-464d-4cfc-9ad0-4e6ff8ef3cda' base_url='https://webpush-staging.mobify.net/api/' endpoint='v1/sites/webpusheen-staging/messages' method='GET' payload=None request_payload='{}' request_headers='{"authorization": "web-ss tlide6g4q2vpv4z3s"}'""",  # noqa
        """INFO 2016-05-19 12:57:18,191 base 3 140567301887808 event='api_client_make_request' request_id='fdad88dc-464d-4cfc-9ad0-4e6ff8ef3cda' base_url='https://webpush-staging.mobify.net/api/' endpoint='v1/sites/webpusheen-staging/messages' method='GET' payload=None request_payload='{}' request_headers='{"authorization": "web-ss tl***************"}'""",  # noqa
    ),
    (
        """base_url='https://cloud-staging.mobify.com/api/' method='GET' payload=None request_payload='{}' request_headers='{"authorization": "Bearer fe823727c8e8a028127f891917293010"}' response_body='{"username":"dbader@mobify.com",""",  # noqa
        """base_url='https://cloud-staging.mobify.com/api/' method='GET' payload=None request_payload='{}' request_headers='{"authorization": "Bearer fe******************************"}' response_body='{"username":"dbader@mobify.com","""  # noqa
    )
])
def test_censor_processor(uncensored, expected):
    processor = CensorSensitiveDataProcessor()
    assert processor(None, None, uncensored) == expected


def test_censor_processor_bad_regex():
    # No "secret" group
    patterns = [r'.*']

    processor = CensorSensitiveDataProcessor(patterns)
    assert processor(None, None, 'my log string') == 'my log string'


def test_censoring_can_be_disabled(settings):
    settings.LOGGING_CENSORSHIP_DISABLED = True

    log = 'MY_API_KEY=f00bar ANOTHER_KEY=12345'
    processed_log = CensorSensitiveDataProcessor()(None, None, log)

    assert processed_log == log
