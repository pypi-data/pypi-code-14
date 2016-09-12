from ahoyhoy.servicediscovery import ServiceDiscoveryHttpClient
from ahoyhoy.utils import Host


class FakeHttpClient():
    def __init__(self):
        pass


def test_url_host_port():
    # Arrange
    host = Host('google.com', '443')
    sd = ServiceDiscoveryHttpClient(host)
    # Assert
    assert sd.url == 'https://google.com:443'
    assert sd.address == 'google.com'
    assert sd.port == '443'
    assert sd.host == host


def test_equal():
    # Arrange
    host = Host('google.com', '443')
    sd = ServiceDiscoveryHttpClient(host)
    sd2 = ServiceDiscoveryHttpClient(host)
    # Assert
    assert sd == sd2
