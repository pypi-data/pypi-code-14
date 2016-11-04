"""
Packages Python functions into a zip or directory for use by AWS Lambda.

    * Installs requirements.
    * Sets build-time environment variables for runtime use.
"""

import contextlib
import os.path
import shutil
import tempfile
import zipfile

from .entrypoint import Entrypoint
from .pip import Pip

class Packager(object):
    """
    Packages a Python function into a zip or directory for use by AWS Lambda.

        * Installs requirements.
        * Sets build-time environment variables for runtime use.
    """

    def __init__(self, handler="index.handler"):
        self.handler = handler

    def to_zip(self, path, handler, dest, *args, **kwargs):
        """
        Package a Lambda function into a zip file.

        Arguments:

            * `path`: Python source path.
            * `handler`: the Lambda handler to import after initialisation,
                             e.g "index.handler"
            * `dest`: Zip output filename.
            * `env`: Dict specifying fixed environment variable values. These
                     will be added to the usual environment variables, and are
                     available through `os.environ`
            * `requirements`: Required packages, e.g ["requests", "flask"]
            * `requirement_files`: Names of requirement files, relative to
                                   `path`.
            * `optional_requirement_files`: Names of optional requirement files,
                                            relative to `path`.
        """

        with zipfile.ZipFile(dest, "w") as zip_file:
            with self.temp_path() as temp_path:
                self.to_dir(path, handler, temp_path, *args, **kwargs)
                self.zip_write_recursive(temp_path, zip_file)

    def to_dir(self, path, handler, dest, env={}, requirements=[], requirement_files=[], optional_requirements_files=["requirements.txt"]):
        """
        Package a Lambda function into a directory. Same arguments as `to_zip`.
        """

        function_path = "function"
        lib_path = "lib"

        shutil.copytree(path, os.path.join(dest, function_path))

        entrypoint_module, _, _ = self.handler.rpartition(".")
        entrypoint = Entrypoint(
            src_handler=handler,
            dst_handler=self.handler,
            chdir=function_path,
            import_paths=[function_path, lib_path],
            env=env
        )
        entrypoint_filename = os.path.join(dest, "{}.py".format(entrypoint_module.replace(".", "/")))
        with open(entrypoint_filename, "w") as fp:
            fp.write(entrypoint.get_content())

        pip = Pip()
        pip.add_requirements(*requirements)
        pip.add_requirement_files(*[
            os.path.join(path, filename)
            for filename in requirement_files
        ])
        pip.add_requirement_files(*[
            os.path.join(path, filename)
            for filename in optional_requirements_files
            if os.path.isfile(os.path.join(path, filename))
        ])
        pip.install(os.path.join(dest, lib_path))

    @contextlib.contextmanager
    def temp_path(self, *args, **kwargs):
        path = tempfile.mkdtemp(*args, **kwargs)
        try:
            yield path
        finally:
            shutil.rmtree(path)

    def zip_write_recursive(self, root, zip_file):
        for path, _, basenames in os.walk(root):
            for basename in basenames:
                filename = os.path.join(root, path, basename)
                zip_file.write(filename, os.path.relpath(filename, root))
