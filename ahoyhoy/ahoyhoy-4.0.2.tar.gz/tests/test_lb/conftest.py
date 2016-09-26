import pytest


from ahoyhoy.lb.providers.iprovider import IProvider
from ahoyhoy.utils import Host


@pytest.fixture
def FakeEmptyProvider():

    class FakeEmptyProviderClass(IProvider):

        def get_list(self):
            return []

    return FakeEmptyProviderClass


@pytest.fixture
def FakeProvider():

    class FakeProviderClass(IProvider):

        def get_list(self):
            return [Host('1', '1'), Host('2', '2'), Host('3', '3')]

    return FakeProviderClass
