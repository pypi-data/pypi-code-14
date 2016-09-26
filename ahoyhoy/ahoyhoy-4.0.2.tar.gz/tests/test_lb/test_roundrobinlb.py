import pytest

from ahoyhoy.endpoints import Endpoint
from ahoyhoy.lb.providers import ListProvider
from ahoyhoy.lb.roundrobinlb import RoundRobinLB
from ahoyhoy.lb.exceptions import LbNoEndpointsException
from ahoyhoy.utils import Host


hostlist = [Host('1', '1'), Host('2', '2'), Host('3', '3')]
endpoint_list = map(Endpoint, hostlist)

def test_roundrobin_resolver_choose_next(FakeEmptyProvider):
    res = RoundRobinLB(FakeEmptyProvider())

    assert res._choose_next() is None


def test_roundrobin_resolver_one_by_one():
    res = RoundRobinLB(ListProvider(*hostlist))

    assert list(endpoint_list) == [res._choose_next() for i in range(3)]


def test_roundrobin_resolver_wrong_provider():
    with pytest.raises(AssertionError):
        RoundRobinLB([])


def test_roundrobin_resolver_pick():
    res = RoundRobinLB(ListProvider(*hostlist))
    assert isinstance(res.pick(), Endpoint)


def test_roundrobin_resolver_empty_pick(FakeEmptyProvider):
    res = RoundRobinLB(FakeEmptyProvider())
    with pytest.raises(LbNoEndpointsException):
        res.pick()
