import logging
import traceback

from apscheduler.schedulers.background import BackgroundScheduler

from python_agent import config
from python_agent.packages import requests
from python_agent.packages.requests import Timeout
from python_agent.utils.sealights_logging import SealightsHTTPHandler


config.app["server"] = "http://someserver/api"


def create_logger_and_mock(mocker):
    mock_post = mocker.patch.object(requests, "post")
    mocker.patch.object(BackgroundScheduler, "start")
    mocker.patch.object(BackgroundScheduler, "shutdown")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = SealightsHTTPHandler(10)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger, mock_post


def test_request_schema(mocker):
    logger, mock_post = create_logger_and_mock(mocker)

    logger.info("some message 1")
    logger.info("some message 2")
    sealights_handler = logger.handlers[0]
    sealights_handler.flush()

    assert mock_post.called
    log_request = mock_post.call_args_list[0][1]["json"]
    assert "customerId" in log_request
    assert "appName" in log_request
    assert "branch" in log_request
    assert "build" in log_request
    assert "creationTime" in log_request
    assert "environment" in log_request
    assert "log" in log_request


def test_request_timeout(mocker):
    logger, mock_post = create_logger_and_mock(mocker)
    mock_post.side_effect = Timeout

    logger.info("some message 1")
    logger.info("some message 2")
    sealights_handler = logger.handlers[0]
    sealights_handler.flush()

    assert mock_post.called


def test_exception_in_log(mocker):
    logger, mock_post = create_logger_and_mock(mocker)

    logger.info("some message 1")
    logger.exception("some message 2")
    sealights_handler = logger.handlers[0]
    sealights_handler.flush()

    assert mock_post.called
    log_request = mock_post.call_args_list[0][1]["json"]
    assert "some message 2" in log_request["log"]


# def test_exception_during_flush(mocker):
#     logger, mock_post = create_logger_and_mock(mocker)
#     mock_post.side_effect = Exception
#     mock_traceback = mocker.patch.object(traceback, "print_exception")
#
#     logger.info("some message 1")
#     sealights_handler = logger.handlers[0]
#     sealights_handler.flush()
#
#     assert mock_traceback.called


def test_close_logger(mocker):
    logger, mock_post = create_logger_and_mock(mocker)
    mock_logging_close = mocker.patch("logging.Handler.close")
    for mock in mocker._mocks:
        if mock._mock_name == "shutdown":
            mock_shutdown = mock
            mock_shutdown.side_effect = Exception

    logger.info("some message 1")
    sealights_handler = logger.handlers[0]
    sealights_handler.flush()
    sealights_handler.close()

    assert mock_logging_close.called
