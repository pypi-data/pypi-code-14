import sys
import os
import logging
import pytest
from copy import deepcopy

import jsonschema

from python_agent.build_scanner import file_signature, main
from python_agent.tests.build_scanner.test_hashing import buildmapping_schema
from python_agent.utils import get_top_relative_path


def test_hashes(before, after, meta, directory):
    assert before
    assert after
    assert meta
    assert meta.has_key("sl_file")

    for method_name, method in before["methods_dict"].items():
        assert meta.has_key(method_name), "meta must contain all methods"
        error_message = "method: %s. case: %s. before: %s. after: %s" \
                        % (method_name, directory, method["hash"], after["methods_dict"][method_name]["hash"])
        if meta[method_name]:
            assert method["hash"] == after["methods_dict"][method_name]["hash"], error_message
        else:
            assert not method["hash"] == after["methods_dict"][method_name]["hash"], error_message
        if meta.get("sl_file"):
            assert before["hash"] == after["hash"]
        else:
            assert not before["hash"] == after["hash"]


def pytest_generate_tests(metafunc):
    if not ["before", "after", "meta", "directory"] == metafunc.fixturenames:
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_params = []
    try:
        rootdir = current_dir + "/cases"
        for subdir, dirs, files in os.walk(rootdir):
            if not set(["before.py", "after.py", "__init__.py"]).issubset(files):
                continue
            parent, directory = subdir.split("/")[-2], subdir.split("/")[-1]
            before = file_signature.calculate_file_signature(subdir + "/before.py", get_top_relative_path(subdir + "/before.py"))
            after = file_signature.calculate_file_signature(subdir + "/after.py", get_top_relative_path(subdir + "/after.py"))

            before["methods_dict"] = dict((method["name"], method) for method in before["methods"])
            after["methods_dict"] = dict((method["name"], method) for method in after["methods"])
            meta = __import__(
                "python_agent.tests.build_scanner.test_hashing.cases.%s.%s.__init__" % (parent, directory),
                fromlist=["meta"]
            ).meta
            test_params.append((before, after, meta, directory))

        metafunc.parametrize("before,after,meta,directory", test_params)

    except Exception as e:
        pytest.fail(msg=str(e))


def test_schema(mocker):
    mock_post = mocker.patch("python_agent.packages.requests.post", spec=True)
    original_argv = deepcopy(sys.argv)
    sys.argv = [
        "sealights-build",
        "--customer_id", "demo",
        "--app_name", "python-agent",
        "--server", "http://dev-shai3.sealights.co:8080/api",
        "--build", "3",
        "--branch", "master",
        "--include", "python_agent/build_scanner*"
    ]
    top_package = __import__(__name__.split('.')[0])
    top_path = os.path.dirname(top_package.__file__)
    os.chdir(top_path)
    main.main()
    assert mock_post.called
    assert len(mock_post.call_args_list) == 1
    body = mock_post.call_args_list[0][1]["json"]
    try:
        jsonschema.validate(body, buildmapping_schema.schema)
    except Exception as e:
        pytest.fail(str(e))
    finally:
        sys.argv = original_argv
