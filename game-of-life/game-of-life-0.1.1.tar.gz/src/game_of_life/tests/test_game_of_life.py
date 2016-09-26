import pytest
import game_of_life


def test_project_defines_author_and_version():
    assert hasattr(game_of_life, '__author__')
    assert hasattr(game_of_life, '__version__')
