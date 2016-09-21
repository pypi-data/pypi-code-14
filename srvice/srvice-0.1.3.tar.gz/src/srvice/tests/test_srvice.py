import pytest
import srvice


def test_project_defines_author_and_version():
    assert hasattr(srvice, '__author__')
    assert hasattr(srvice, '__version__')
