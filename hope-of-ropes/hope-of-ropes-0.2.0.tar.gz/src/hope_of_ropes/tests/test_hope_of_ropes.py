import pytest
import hope_of_ropes


def test_project_defines_author_and_version():
    assert hasattr(hope_of_ropes, '__author__')
    assert hasattr(hope_of_ropes, '__version__')
