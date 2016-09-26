import pytest


from ..utils import Host

from .fakes import (
    FakeSession,
    FakeProvider
)


from ahoyhoy.lb.providers import ListProvider
from ahoyhoy.client import Client, LBClientBuilder, SessionClientBuilder
from ahoyhoy.client.exceptions import ClientNoEndpointsException
from ahoyhoy.endpoints import Endpoint
from ahoyhoy.lb import RoundRobinLB


def test_client_builder():
    rrlb = RoundRobinLB(ListProvider(Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)))
    client = LBClientBuilder().add_lb(rrlb).build()

    assert isinstance(client, Client)
    assert client.get('/').status_code == 200


def test_client_builder_with_session():
    client = SessionClientBuilder().add_session(FakeSession()).build()
    assert isinstance(client, Endpoint)
    assert isinstance(client._session, FakeSession)


def test_client_builder_with_fake_sesssion():
    client = SessionClientBuilder().add_session(FakeSession()).build()
    response = client.get('/')

    assert response.text == 'Some response'


def test_client_builder_with_non_responsive_sesssion():
    rrlb = RoundRobinLB(FakeProvider())
    client = LBClientBuilder().add_lb(rrlb).build()

    with pytest.raises(ClientNoEndpointsException):
        client.get('/')


def test_client_builder_with_non_responsive_sesssion_and_retries():
    rrlb = RoundRobinLB(FakeProvider())
    client = LBClientBuilder().add_lb(rrlb).set_endpoint_updates(2).build()
    response = client.get('/')

    assert response.status_code == 200
