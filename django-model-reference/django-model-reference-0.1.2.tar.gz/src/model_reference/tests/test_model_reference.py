import pytest
import model_reference


def test_project_defines_author_and_version():
    assert hasattr(model_reference, '__author__')
    assert hasattr(model_reference, '__version__')
