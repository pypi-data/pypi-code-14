"""
Create an entrypoint that sets up the Lambda environment:

    * Change current directory.
    * Configure import paths.
    * Set environment variables.
"""

import textwrap

class Entrypoint(object):
    TEMPLATE = textwrap.dedent("""
        # coding: {encoding}

        import os
        import sys

        ROOT = os.path.abspath(os.path.dirname(__file__))

        sys.path = [
            os.path.join(ROOT, path)
            for path in {import_paths!r}
        ] + sys.path

        if {chdir!r}:
            os.chdir(os.path.join(ROOT, {chdir!r}))

        os.environ.update({env!r})

        del sys.modules[__name__]
        from {src_handler_module} import {src_handler_attr} as {dst_handler_attr}
    """).strip()

    ENCODING = "utf8"

    def __init__(self, src_handler, dst_handler, chdir=None, import_paths=[], env={}):
        """
        Create an entrypoint that sets up the Lambda environment:

            * Change current directory.
            * Configure import paths.
            * Set environment variables.

        Argument:
            * `src_handler`: the Lambda handler to import after initialisation,
                             e.g "index.handler"
            * `dst_handler`: the name of the entrypoint Lambda handler, must be
                             referred to when uploading to AWS.
                             e.g "entrypoint.handler".
            * `chdir`: Desired current directory before running the Lambda
                       handler. Relative to the entrypoint path.
            * `import_paths`: Additional Python import paths. Will be added
                              to the top of the path list.
            * `env`: Dict specifying fixed environment variable values. These
                     will be added to the usual environment variables, and are
                     available through `os.environ`
        """

        self.src_handler = src_handler
        self.dst_handler = dst_handler
        self.chdir = chdir
        self.import_paths = import_paths
        self.env = env

    def get_content(self):
        """
        Get the entrypoint Python source.
        """

        src_handler_module, _, src_handler_attr = self.src_handler.rpartition(".")
        _,  _, dst_handler_attr = self.dst_handler.rpartition(".")

        # TODO: Check handler module/attr are valid format.

        return self.TEMPLATE.format(
            encoding=self.ENCODING,
            src_handler_module=src_handler_module,
            src_handler_attr=src_handler_attr,
            dst_handler_attr=dst_handler_attr,
            chdir=self.chdir,
            import_paths=self.import_paths,
            env=self.env
        ).encode(self.ENCODING)
