import pytest


@pytest.fixture
def sulfur():
    return 'sulfur'


@pytest.fixture
def urlchecker():
    """
    Return the sulfur.urlchecker module.
    """

    import sulfur.urlchecker
    return sulfur.urlchecker
