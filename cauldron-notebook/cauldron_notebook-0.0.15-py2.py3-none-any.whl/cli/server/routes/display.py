import os
import mimetypes

import cauldron
from cauldron.cli.server import run as server_run
import flask


@server_run.APPLICATION.route('/view/<path:route>', methods=['GET', 'POST'])
def view(route: str):

    project = cauldron.project.internal_project
    results_path = project.results_path

    path = os.path.join(results_path, route)
    if not os.path.exists(path):
        return None

    return flask.send_file(
        path,
        mimetype=mimetypes.guess_type(path)[0]
    )
