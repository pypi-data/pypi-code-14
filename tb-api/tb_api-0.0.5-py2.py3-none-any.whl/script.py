from os.path import abspath, dirname, join, exists

import sys

from tb_api.main import load_app


def error_exit_msg(message):
    print(message)
    sys.exit(-1)


def start(base_name, module_suffix='Service', project_dir=".", debug=True, port=5000):
    if not exists(project_dir):
        error_exit_msg("Invalid project %s" % project_dir)

    project_dir = abspath(project_dir)

    static_folder = join(project_dir, 'static')

    app = load_app(base_name, module_suffix=module_suffix,
                   static_folder=static_folder, project_dir=project_dir)
    app.run(debug=debug, port=port)
