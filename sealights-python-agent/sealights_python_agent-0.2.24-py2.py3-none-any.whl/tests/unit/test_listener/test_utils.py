import platform

from python_agent.test_listener.utils import get_test_name_from_identifier, get_execution_id_from_identifier
from python_agent.test_listener.utils import create_environment


def test_get_test_name_from_identifier_empty():
    test_name = get_test_name_from_identifier("")
    assert test_name == ""


def test_get_test_name_from_identifier_null():
    test_name = get_test_name_from_identifier(None)
    assert test_name == ""


def test_get_test_name_from_identifier_no_slash():
    test_name = get_test_name_from_identifier("abc")
    assert test_name == "abc"


def test_get_test_name_from_identifier_one_slash():
    test_name = get_test_name_from_identifier("ab/c")
    assert test_name == "c"


def test_get_test_name_from_identifier_two_slashes():
    test_name = get_test_name_from_identifier("a/b/c")
    assert test_name == "b/c"


def test_get_execution_id_from_identifier_no_slash():
    execution_id = get_execution_id_from_identifier("abc")
    assert execution_id == "abc"


def test_get_execution_id_from_identifier_one_slash():
    execution_id = get_execution_id_from_identifier("ab/c")
    assert execution_id == "ab"


def test_get_execution_id_from_identifier_two_slashes():
    execution_id = get_execution_id_from_identifier("a/b/c")
    assert execution_id == "a"


def test_get_execution_id_from_identifier_empty():
    execution_id = get_execution_id_from_identifier("")
    assert execution_id == ""


def test_get_execution_id_from_identifier_null():
    execution_id = get_execution_id_from_identifier(None)
    assert execution_id == ""


def test_fail_create_environment(mocker):
    mock_platform_machine = mocker.patch.object(platform, "machine")
    mock_platform_machine.side_effect = Exception
    env = create_environment()
    assert env
