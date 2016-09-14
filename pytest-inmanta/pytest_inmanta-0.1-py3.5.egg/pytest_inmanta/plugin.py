"""
    Copyright 2016 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import tempfile
import os
import shutil
import sys
import io

from inmanta import compiler, module, export, config
import pytest


CURDIR = os.getcwd()


def get_module_info():
    curdir = CURDIR
    # Make sure that we are executed in a module
    dir_path = curdir.split(os.path.sep)
    while not os.path.exists(os.path.join("/", *dir_path, "module.yml")) and len(dir_path) > 0:
        dir_path.pop()

    if len(dir_path) == 0:
        raise Exception("Module test case have to be saved in the module they are intended for. "
                        "%s not part of module path" % curdir)

    module_dir = os.path.join("/", *dir_path)
    module_name = dir_path[-1]

    return module_dir, module_name


@pytest.fixture
def project():
    """
        A test fixture that creates a new inmanta project with the current module in. The returned object can be used
        to add files to the unittest module, compile a model and access the results, stdout and stderr.
    """
    _sys_path = sys.path
    _test_project_dir = tempfile.mkdtemp()
    os.mkdir(os.path.join(_test_project_dir, "libs"))

    repos = []
    if "INMANTA_MODULE_REPO" in os.environ:
        repos = os.environ["INMANTA_MODULE_REPO"].split(" ")

    with open(os.path.join(_test_project_dir, "project.yml"), "w+") as fd:
        fd.write("""name: testcase
description: Project for testcase
repo: [%(repo)s]
modulepath: libs
downloadpath: libs
""" % {"repo": ", ".join(repos)})

    # copy the current module in
    module_dir, module_name = get_module_info()
    shutil.copytree(module_dir, os.path.join(_test_project_dir, "libs", module_name))

    test_project = Project()

    # create the unittest module
    test_project.create_module("unittest")

    yield test_project

    shutil.rmtree(_test_project_dir)
    sys.path = _sys_path


class Project():
    """
        This class provides a TestCase class for creating module unit tests. It uses the current module and loads required
        modules from the provided repositories. Additional repositories can be provided by setting the INMANTA_MODULE_REPO
        environment variable. Repositories are separated with spaces.
    """
    def __init__(self):
        self._test_project_dir = None
        self._stdout = None
        self._stderr = None
        self._sys_path = None
        self.types = None
        self.version = None
        self.resources = None
        self._exporter = None

    def create_module(self, name, initcf="", initpy=""):
        module_dir = os.path.join(self._test_project_dir, "libs", name)
        os.mkdir(module_dir)
        os.mkdir(os.path.join(module_dir, "model"))
        os.mkdir(os.path.join(module_dir, "files"))
        os.mkdir(os.path.join(module_dir, "templates"))
        os.mkdir(os.path.join(module_dir, "plugins"))

        with open(os.path.join(module_dir, "model", "_init.cf"), "w+") as fd:
            fd.write(initcf)

        with open(os.path.join(module_dir, "plugins", "__init__.py"), "w+") as fd:
            fd.write(initpy)

        with open(os.path.join(module_dir, "module.yml"), "w+") as fd:
            fd.write("""name: unittest
version: 0.1
license: Test License
            """)

    def compile(self, main):
        """
            Compile the configuration model in main. This method will load all required modules.
        """
        # write main.cf
        with open(os.path.join(self._test_project_dir, "main.cf"), "w+") as fd:
            fd.write(main)

        # compile the model
        config.Config.load_config()
        test_project = module.Project(self._test_project_dir)
        module.Project.set(test_project)

        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            stdout = io.StringIO()
            stderr = io.StringIO()

            sys.stdout = stdout
            sys.stderr = stderr

            (types, scopes) = compiler.do_compile()

            exporter = export.Exporter()
            version, resources = exporter.run(types, scopes)

            self.version = version
            self.resources = resources
            self.types = types
            self._exporter = exporter

            self._stdout = stdout.getvalue()
            self._stderr = stderr.getvalue()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def get_stdout(self):
        return self._stdout

    def get_stderr(self):
        return self._stderr

    def add_mock_file(self, subdir, name, content):
        """
            This method can be used to register mock templates or files in the virtual "unittest" module.
        """
        dir_name = os.path.join(self._test_project_dir, "libs", "unittest", subdir)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        with open(os.path.join(dir_name, name), "w+") as fd:
            fd.write(content)
