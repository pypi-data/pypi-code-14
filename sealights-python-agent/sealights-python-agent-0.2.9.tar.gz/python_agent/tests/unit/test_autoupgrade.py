import os

import pkg_resources
from pip import status_codes
from pip.commands import InstallCommand

from python_agent.packages import requests
from python_agent import config
from python_agent.packages import semantic_version
from python_agent.utils.autoupgrade import AutoUpgrade


def test_same_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.1")

    status = auto_upgrade.upgrade()

    assert status == status_codes.ERROR


def test_new_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")

    auto_upgrade.upgrade()

    assert mock_install.call_count == 1
    assert mock_install.call_args_list[0][0][0] == semantic_version.Version("0.1.2")


def test_old_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.3.2")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")

    auto_upgrade.upgrade()

    assert mock_install.call_count == 1
    assert mock_install.call_args_list[0][0][0] == semantic_version.Version("0.1.2")


def test_fail_get_version_from_server(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")

    auto_upgrade.upgrade()

    assert mock_install.call_count == 1
    assert mock_install.call_args_list[0][0][0] == semantic_version.Version("0.1.2")


def test_exception_on_install(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")
    mock_install.side_effect = Exception
    mock_restart = mocker.patch.object(auto_upgrade, "restart")

    status = auto_upgrade.upgrade()

    assert status == status_codes.ERROR
    assert not mock_restart.called


def test_failed_install(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")
    mock_install.return_value = status_codes.ERROR
    mock_restart = mocker.patch.object(auto_upgrade, "restart")

    status = auto_upgrade.upgrade()

    assert status == status_codes.ERROR
    assert not mock_restart.called


def test_install(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_run = mocker.patch.object(InstallCommand, "run")
    mock_run.return_value = status_codes.SUCCESS

    status = auto_upgrade.install(semantic_version.Version("0.1.2"))

    assert status == status_codes.SUCCESS
    assert mock_run.called
    assert mock_run.call_count == 1


def test_restart(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")
    mock_install.return_value = status_codes.SUCCESS
    mock_execl = mocker.patch.object(os, "execl")

    status = auto_upgrade.upgrade()

    assert status == status_codes.SUCCESS
    assert mock_execl.called
    assert mock_execl.call_count == 1


def test_failed_restart(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(auto_upgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_install = mocker.patch.object(auto_upgrade, "install")
    mock_install.return_value = status_codes.SUCCESS
    mock_execl = mocker.patch.object(os, "execl")
    mock_execl.side_effect = Exception

    status = auto_upgrade.upgrade()

    assert status == status_codes.ERROR
    assert mock_execl.called
    assert mock_execl.call_count == 1


def test_get_recommended_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", "http://someserver/api", config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_requests_get = mocker.patch.object(requests, "get")
    mock_response = mocker.patch.object(requests, "Response")
    mock_response.json.return_value = {
        'agent': {
            'version': '0.1.2'
        }
    }
    mock_requests_get.return_value = mock_response

    version = auto_upgrade.get_recommended_version()

    assert version == semantic_version.Version("0.1.2")


def test_failed_get_recommended_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", "http://someserver/api", config.app["customer_id"])
    mock_current_version = mocker.patch.object(auto_upgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_requests_get = mocker.patch.object(requests, "get")
    mock_response = mocker.patch.object(requests, "Response")
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    version = auto_upgrade.get_recommended_version()

    assert version == semantic_version.Version("0.1.1")


def test_get_current_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", "http://someserver/api", config.app["customer_id"])
    mock_get_distribution = mocker.patch.object(pkg_resources, "get_distribution")
    mock_get_distribution.return_value.version = "0.1.1"

    version = auto_upgrade.get_current_version()

    assert version == semantic_version.Version("0.1.1")


def test_failed_get_current_version(mocker):
    auto_upgrade = AutoUpgrade("sealights-python-agent", "http://someserver/api", config.app["customer_id"])
    mock_get_distribution = mocker.patch.object(pkg_resources, "get_distribution")
    mock_get_distribution.side_effect = Exception

    version = auto_upgrade.get_current_version()

    assert version == semantic_version.Version("0.0.0")
