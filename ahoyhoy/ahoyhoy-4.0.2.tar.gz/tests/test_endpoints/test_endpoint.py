import requests
from ahoyhoy.endpoints import Endpoint, SimpleHttpEndpoint
from ahoyhoy.servicediscovery import ServiceDiscoveryHttpClient
from ahoyhoy.utils import Host


import pytest

host = Host('google.com', '80')


def test_closed_endpoint():
    # Arrange
    e = Endpoint(host)
    # Act
    e.open()
    # Assert
    with pytest.raises(RuntimeError):
        e.get("/cat")


def test_simplehttpendpoint():
    # Arrange
    e = SimpleHttpEndpoint()
    # Assert
    assert isinstance(e._session, requests.Session)


def test_hardsimplehttpendpoint():
    """
    Prove SimpleHttpEndpoint works by making it not-so-simple
    """
    # Arrange
    sdhc = ServiceDiscoveryHttpClient(host)
    # Act
    ep = SimpleHttpEndpoint(session=sdhc, retry='foo')
    # Assert
    assert ep._session == sdhc


def test_passed_session_and_host_are_correct():
    """
    Be sure that if you pass a host and a session, that the correct thing (just assignment)
    is done with both.
    """
    # Arrange
    sess = requests.Session()
    # Act
    e = Endpoint(host=host, session=sess)
    # Assert
    # because session here is ServiceDiscoveryHttpClient, it has session at its attribute
    assert e._session._session == sess
    assert e._host == host


def test_passed_host_with_default_session_is_correct():
    """
    Be sure that if you pass a host, but use the default session, that you get the correctly
    set session.
    """
    # Arrange & Act
    e = Endpoint(host=host)
    # Assert
    assert e._host == host
    assert e._session._host == host
