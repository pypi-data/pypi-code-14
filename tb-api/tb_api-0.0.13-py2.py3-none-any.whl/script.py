import logging
import sys
from os.path import abspath, join, exists

from tb_api.main import load_app


def error_exit_msg(message):
    print(message)
    sys.exit(-1)


def start(config):
    """

    :param config:
    :type config: tb_api.model.Config
    :return:
    """
    project_dir = config.project_dir
    port = config.port
    debug = config.debug

    if not exists(project_dir):
        error_exit_msg("Invalid project %s" % project_dir)

    project_dir = abspath(project_dir)

    static_folder = join(project_dir, 'static')

    app = load_app(config.loader,
                   static_folder=static_folder, project_dir=project_dir)
    try:
        app.run(host='0.0.0.0', debug=debug, port=port)
    except Exception as e:
        if debug:
            logging.exception(e)

        error_exit_msg('Could not run on port {0}: {1}'.format(port, str(e)))
