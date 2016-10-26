import os
import sys
from copy import deepcopy

import jsonschema
import pytest

from python_agent.tests.component.data import buildmapping_schema
from python_agent import admin


def test_schema(mocker):
    mock_post = mocker.patch("python_agent.packages.requests.post", spec=True)
    original_argv = deepcopy(sys.argv)
    sys.argv = [
        "sealights-admin",
        "--customer_id", "demo",
        "--app_name", "python-agent",
        "--server", "http://dev-shai3.sealights.co:8080/api",
        "--build", "3",
        "--branch", "master",
        "--source", "python_agent",
        "--include", "python_agent/build_scanner*",
        "build"
    ]
    top_package = __import__(__name__.split('.')[0])
    top_path = os.path.dirname(top_package.__file__)
    os.chdir(top_path)
    try:
        admin.cli()
    except SystemExit as e:
        if getattr(e, "code", 1) != 0:
            raise
    assert mock_post.called
    assert len(mock_post.call_args_list) == 1
    body = mock_post.call_args_list[0][1]["json"]
    try:
        jsonschema.validate(body, buildmapping_schema.schema)
    except Exception as e:
        pytest.fail(str(e))
    finally:
        sys.argv = original_argv
