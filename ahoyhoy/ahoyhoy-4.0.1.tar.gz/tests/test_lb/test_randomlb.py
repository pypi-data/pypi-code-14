import pytest

from ahoyhoy.lb.randomlb import RandomLB
from ahoyhoy.utils import Host
from ahoyhoy.endpoints import Endpoint
from ahoyhoy.lb.exceptions import NoAvailableEndpointsLbException


def test_random_resolver_choose_next(FakeEmptyProvider):
    res = RandomLB(FakeEmptyProvider())

    assert res._choose_next() is None


def test_random_resolver_random_overload(FakeProvider):
    def first(x, size):
        return 1
    res = RandomLB(FakeProvider(), random_function=first)

    # create_endpoint is a classmethod
    assert res._choose_next() == res.get_or_create_endpoint(Host('2', '2'))


def test_random_resolver_wrong_provider():
    with pytest.raises(AssertionError):
        RandomLB([])


def test_random_resolver_pick(FakeProvider):
    def first(x, size):
        return 1
    res = RandomLB(FakeProvider(), first)
    assert isinstance(res.pick(), Endpoint)


def test_random_resolver_empty_pick(FakeEmptyProvider):
    res = RandomLB(FakeEmptyProvider())
    with pytest.raises(NoAvailableEndpointsLbException):
        res.pick()