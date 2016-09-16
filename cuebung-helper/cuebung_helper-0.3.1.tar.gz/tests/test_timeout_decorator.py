"""Timeout decorator tests."""
import time

import pytest

from cuebung_helper.timeout_decorator import timeout, MyTimeoutError


@pytest.fixture(params=[False, True])
def use_signals(request):
    """Use signals for timing out or not."""
    return request.param


def test_timeout_decorator_arg(use_signals):
    """Test"""
    @timeout(1, use_signals=use_signals)
    def func():
        """Test function"""
        time.sleep(2)
    with pytest.raises(MyTimeoutError):
        func()


def test_timeout_kwargs(use_signals):
    """Test"""
    @timeout(3, use_signals=use_signals)
    def func():
        """Test function"""
        time.sleep(2)
    with pytest.raises(MyTimeoutError):
        func(timeout=1)  # pylint: disable=E1123


def test_timeout_no_seconds(use_signals):
    """Test"""
    @timeout(use_signals=use_signals)
    def func():
        """Test function"""
        time.sleep(0.1)
    func()


def test_timeout_partial_seconds(use_signals):
    """Test"""
    @timeout(0.2, use_signals=use_signals)
    def func():
        """Test function"""
        time.sleep(0.5)
    with pytest.raises(MyTimeoutError):
        func()


def test_timeout_ok(use_signals):
    """Test"""
    @timeout(seconds=2, use_signals=use_signals)
    def func():
        """Test function"""
        time.sleep(1)
    func()


def test_function_name(use_signals):
    """Test"""
    @timeout(seconds=2, use_signals=use_signals)
    def func_name():
        """Test function"""
        pass

    assert func_name.__name__ == 'func_name'


def test_timeout_pickle_error():
    """Test that when a pickle error occurs a timeout error is raised."""
    @timeout(seconds=1, use_signals=False)
    def func():
        """Test function"""
        time.sleep(0.1)

        class Test(object):
            """Test class"""
            pass
        return Test()
    with pytest.raises(MyTimeoutError):
        func()
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
