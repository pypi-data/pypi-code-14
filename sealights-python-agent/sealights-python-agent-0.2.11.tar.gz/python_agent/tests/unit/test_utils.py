from argparse import ArgumentTypeError
import pkg_resources

import pytest

from python_agent.packages import requests
from python_agent.utils import validate_server_api, validate_server, get_config_from_server


def test_validate_server_api_http(mocker):
    return_value = validate_server_api("http://someserver")
    assert return_value


def test_validate_server_api_https(mocker):
    return_value = validate_server_api("https://someserver")
    assert return_value


def test_validate_server_api_validate_api_correct1(mocker):
    return_value = validate_server("https://someserver/api")
    assert return_value


def test_validate_server_api_validate_api_correct2(mocker):
    return_value = validate_server("https://someserver/api/")
    assert return_value


def test_validate_server_api_bad_format(mocker):
    with pytest.raises(ArgumentTypeError):
        validate_server_api("h1ttps://someserver")


def test_validate_server_api_not_http_or_https(mocker):
    with pytest.raises(ArgumentTypeError):
        validate_server_api("ftp://someserver")


def test_validate_server_api_validate_api(mocker):
    with pytest.raises(ArgumentTypeError):
        validate_server("https://someserver")


def test_get_config_from_server_failed(mocker):
    mocker.patch.object(requests, "get")
    mock_get_distribution = mocker.patch.object(pkg_resources, "get_distribution")
    mock_get_distribution.return_value.version = "0.1.1"

    server_config = get_config_from_server("http://someserver/api", "customer_id", "app_name", "branch", "env")

    assert server_config == {}


def test_get_config_from_server(mocker):
    mock_requests_get = mocker.patch.object(requests, "get")
    mock_get_distribution = mocker.patch.object(pkg_resources, "get_distribution")
    mock_get_distribution.return_value.version = "0.1.1"
    mock_response = mocker.patch.object(requests, "Response")
    mock_response.json.return_value = {'config': '{"logging": "{}"}'}
    mock_requests_get.return_value = mock_response

    server_config = get_config_from_server("http://someserver/api", "customer_id", "app_name", "branch", "env")

    assert server_config == {'logging': '{}'}
