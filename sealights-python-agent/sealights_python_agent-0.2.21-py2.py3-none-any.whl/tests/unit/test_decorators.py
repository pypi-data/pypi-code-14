import logging
import os
import time

from python_agent.build_scanner.file_signature import calculate_file_signature
from python_agent.utils import get_top_relative_path, retries, exception_handler


def test_exception_handler(mocker):
    mock_ast_parse = mocker.patch("python_agent.utils.ast_utils.parse")
    mock_ast_parse.side_effect = Exception("test_exception_handler")
    log = logging.getLogger("python_agent.build_scanner.file_signature")
    mock_logger = mocker.patch.object(log, "exception")

    full_path = os.path.realpath(__file__)
    calculate_file_signature(full_path, get_top_relative_path(full_path))

    assert mock_logger.called
    assert len(mock_logger.call_args_list) == 1
    error_message = mock_logger.call_args_list[0][0][0]
    assert "file signature" in error_message
    assert "Args" in error_message
    assert "Kwargs" in error_message
    assert "test_exception_handler" in error_message


def test_exception_handler_not_quiet(mocker):
    log = logging.getLogger(__name__)
    function = lambda x: 1 / 0
    mock_logger = mocker.patch.object(log, "exception")

    try:
        exception_handler(log, quiet=False, message="failed running function")(function)(1)
    except Exception as e:
        assert type(e) == ZeroDivisionError

    assert mock_logger.called
    assert len(mock_logger.call_args_list) == 1
    error_message = mock_logger.call_args_list[0][0][0]
    assert "failed running function" in error_message
    assert "Args" in error_message
    assert "Kwargs" in error_message


def test_number_of_retries(mocker):
    tries = 3
    mock_sleep = mocker.patch.object(time, "sleep")
    function = lambda x: 1 / 0
    decorator = retries(logging.getLogger(__name__), tries=tries)(function)

    try:
        decorator(5)
    except Exception as e:
        assert type(e) == ZeroDivisionError
    assert mock_sleep.call_count == tries
