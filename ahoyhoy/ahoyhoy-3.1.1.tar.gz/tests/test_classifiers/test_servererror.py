import pytest
from ahoyhoy.classifiers import raise_for_status
from ahoyhoy.classifiers.exceptions import Ahoyhoy500Exception


class FakeResponse(object):
    def __init__(self, code):
        self.status_code = code
        self.reason = "reason"
        self.url = "url"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def test_server_error_valid_response():
    obj = FakeResponse(499)
    obj2 = FakeResponse(600)

    assert raise_for_status(obj) == obj
    assert raise_for_status(obj2) == obj2


def test_server_error():
    obj = FakeResponse(500)
    obj2 = FakeResponse(599)

    with pytest.raises(Ahoyhoy500Exception) as e:
        raise_for_status(obj)
        assert e.code == 500
        assert e.reason == 'reason'
        assert e.url == 'url'

    with pytest.raises(Ahoyhoy500Exception) as e:
        raise_for_status(obj2)
        assert e.code == 599
        assert e.reason == 'reason'
        assert e.url == 'url'
