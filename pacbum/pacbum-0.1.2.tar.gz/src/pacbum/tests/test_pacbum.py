import pytest
import pacbum


def test_project_defines_author_and_version():
    assert hasattr(pacbum, '__author__')
    assert hasattr(pacbum, '__version__')
