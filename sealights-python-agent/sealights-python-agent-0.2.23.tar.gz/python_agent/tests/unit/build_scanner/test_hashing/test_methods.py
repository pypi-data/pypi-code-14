import os

import pytest

from python_agent.build_scanner import file_signature
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
                "python_agent.tests.unit.build_scanner.test_hashing.cases.%s.%s.__init__" % (parent, directory),
                fromlist=["meta"]
            ).meta
            test_params.append((before, after, meta, directory))

        metafunc.parametrize("before,after,meta,directory", test_params)

    except Exception as e:
        pytest.fail(msg=str(e))


def test_position():
    data_dir = os.path.dirname(os.path.abspath(__file__)) + "/data"
    result = file_signature.calculate_file_signature(
        data_dir + "/position_methods.py", get_top_relative_path(data_dir + "/position_methods.py"))
    for method in result["methods"]:
        if method["name"] == "foo":
            assert method["position"] == [19, 0]
        if method["name"] == "bar":
            assert method["position"] == [24, 0]
        if method["name"] == "sum_two":
            assert method["position"] == [28, 0]
