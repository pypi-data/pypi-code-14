import pytest


from ..utils import Host

from .fakes import (
    FakeSession,
    FakeProvider
)


from ahoyhoy.lb.providers import ListProvider
from ahoyhoy.client import Client, ClientBuilder
from ahoyhoy.client.exceptions import NoAvailableEndpointsClientException
from ahoyhoy.endpoints import Endpoint
from ahoyhoy.lb import RoundRobinLB


def test_client_builder():
    rrlb = RoundRobinLB(ListProvider(Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)))
    client = ClientBuilder.with_lb(rrlb)

    assert isinstance(client, Client)
    assert client.get('/').status_code == 200


def test_client_builder_with_session():
    client = ClientBuilder.with_session('bla')
    assert isinstance(client, Endpoint)
    assert isinstance(client._session, str)


def test_client_builder_with_fake_sesssion():
    client = ClientBuilder.with_session(FakeSession())
    response = client.get('/')

    assert response.text == 'Some response'


def test_client_builder_with_non_responsive_sesssion():
    rrlb = RoundRobinLB(FakeProvider())
    client = ClientBuilder.with_lb(rrlb)

    with pytest.raises(NoAvailableEndpointsClientException):
        client.get('/')


def test_client_builder_with_non_responsive_sesssion_and_retries():
    rrlb = RoundRobinLB(FakeProvider())
    client = ClientBuilder.with_lb(rrlb, ep_list_update_tries=2)
    response = client.get('/')

    assert response.status_code == 200
