import pytest

from ahoyhoy.circuit import Circuit, ClosedState, OpenState
from requests.exceptions import ConnectionError, ConnectTimeout
from retry.api import retry_call


def _default_retry(f, fargs=None, fkwargs=None):
    _exceptions = (ConnectionError, ConnectTimeout)
    _tries = 3
    _delay = 0
    _max_delay = None
    _backoff = 1.5
    _jitter = 0
    response = retry_call(f, fargs=fargs, fkwargs=fkwargs, exceptions=_exceptions, tries=_tries)
    return response


class FakeService(object):
    def __init__(self):
        self.calls = 0
        self.status_code = 200
    
    def sample_func(self, *args, **kwargs):
        if self.calls == 0:
            self.calls += 1
            raise ConnectionError
        return self


def test_create():
    # Arrange & Act
    cb = Circuit()
    # Assert
    assert cb._state == ClosedState

def test_change_state():
    # Arrange
    cb = Circuit()
    # Act
    cb.change_state(OpenState)
    # Assert
    assert cb._state == OpenState

def test_closed_methods():
    # Arrange & Act
    cb = Circuit()
    assert cb._state == ClosedState
    with pytest.raises(RuntimeError):
        cb.close()

    cb.open()
    assert cb._state == OpenState

def test_open_methods():
    # Arrange
    cb = Circuit()
    # Act
    cb.open()
    assert cb._state == OpenState

    with pytest.raises(RuntimeError):
        cb.open()

    cb.close()
    assert cb._state == ClosedState

def test_state_classify_exc():
    # Arrange
    pass

def test_state_classify_retry():
    # Arrange
    cb = Circuit()
    cb._retry = _default_retry
    s = FakeService()

    # Act
    cb.classify(s.sample_func, 1, a=2)

