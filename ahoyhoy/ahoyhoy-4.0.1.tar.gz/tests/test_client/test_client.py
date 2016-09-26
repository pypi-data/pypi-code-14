import pytest


from ..test_client.fakes import (
    FakeLoadBalancer,
    FakeLoadBalancer2EPs,
    FakeFailedService,
    FakeProvider
)

from ..utils import Host


from ahoyhoy.lb.providers import ListProvider
from ahoyhoy.client import Client
from ahoyhoy.endpoints import Endpoint
from ahoyhoy.lb import RoundRobinLB
from ahoyhoy.client.exceptions import NoAvailableEndpointsClientException


def test_client_some_bad_hosts():
    rrlb = RoundRobinLB(ListProvider(Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)))
    client = Client(rrlb)
    assert client.get('/').status_code == 200


def test_client_no_good_hosts():
    rrlb = RoundRobinLB(ListProvider(Host('badhost2.bla', 80), Host('google1.com1', 80), Host('badhost3.bla', 80)))
    client = Client(rrlb)
    with pytest.raises(NoAvailableEndpointsClientException):
        client.get('/')


def test_client_headers():
    rrlb = RoundRobinLB(ListProvider(Host('google.com', 80)))
    client = Client(rrlb)
    response = client.get('/', headers={'bla': 'foo'})
    assert 'bla' in response.request.headers.keys()
    assert 'foo' in response.request.headers.values()


def test_client_resolve():
    """Tests the client.resolve() function"""
    # Arrange
    e = Endpoint(Host('0.0.0.0', '443'))
    client = Client(FakeLoadBalancer([e, ]))
    # Act
    assert client.resolve() == e


def test_client_resolve_proxy_fail():
    # Arrange
    e = Endpoint(Host('0.0.0.0', '443'))
    client = Client(FakeLoadBalancer([e, ]))
    # Act
    with pytest.raises(AttributeError):
        assert client.willfail()


def test_client_uninstantiated_loadbalancer():
    with pytest.raises(TypeError):
        Client(FakeLoadBalancer)


def test_client_NO_http_methods():
    e = Endpoint(Host('0.0.0.0', '443'))
    client = Client(FakeLoadBalancer([e, ]))
    with pytest.raises(AttributeError):
        client.mount('https://', 'foo')


def test_client_new_endpoint_every_time():
    e1 = Endpoint(Host('0.0.0.1', '443'))
    e1.get = lambda x: 'Response from the first EP'

    e2 = Endpoint(Host('0.0.0.2', '443'))
    e2.get = lambda x: 'Response from the second EP'
    client = Client(FakeLoadBalancer2EPs(endpoints_lst=(e1, e2)))

    resp = client.get('/')
    assert resp == 'Response from the first EP'

    resp = client.get('/')
    assert resp == 'Response from the second EP'

    resp = client.get('/')
    assert resp == 'Response from the first EP'


def test_client_retries():
    e = Endpoint(Host('0.0.0.1', '443'))
    e.get = FakeFailedService().get
    client = Client(FakeLoadBalancer([e, ]))

    resp = client.get('/')
    assert resp == 'Good response'


def test_client_no_endpoints():
    rrlb = RoundRobinLB(FakeProvider())
    client = Client(rrlb)

    with pytest.raises(NoAvailableEndpointsClientException):
        client.get('/')


def test_client_no_endpoints_retry():
    rrlb = RoundRobinLB(FakeProvider())
    client = Client(rrlb, ep_list_update_tries=2)
    resp = client.get('/')

    assert resp.status_code == 200
