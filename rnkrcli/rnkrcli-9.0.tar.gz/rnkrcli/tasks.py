import copy
import base64
import json

from .consts import RNKR_FILE, RNKRRC_FILE
from .utils import get_artifact_settings, create_project_zip, render_template
from .rnkrsvc import create_artifact, run_artifact, get_artifact

execution_to_pk = {
    'python': 1,
    'r': 2
}

artifact_kind_to_pk = {
    'app': 1,
    'widget': 2,
    'service': 3
}

execution_to_files = {
    'python': {
        'app.py.tpl': {
            'to': '{mnemonic}.py',
        },
        'config.rnkr.python.tpl': {
            'to': 'rnkr'
        },
        'requirements.txt.tpl': {
            'to': 'requirements.txt'
        }
    },
    'r': {
        'app.r.tpl': {
            'to': '{mnemonic}.r'
        },
        'config.rnkr.r.tpl': {
            'to': 'rnkr'
        },
    }
}


def __store_artifact(artifact):
    with open('.artifact', 'w') as f:
        f.write(json.dumps({'pk': artifact['pk']}))


def create_project(mnemonic, execution, artifact):
    mnemonic = mnemonic.lower()
    if execution not in execution_to_files:
        raise Exception('execution `{0}` is not supported'.format(execution))

    context = {
        'mnemonic': mnemonic,
        'engine': execution_to_pk[execution],
        'artifact': artifact_kind_to_pk[artifact]
    }

    for k, v in execution_to_files[execution].iteritems():
        render_template(k, context, v['to'].format(mnemonic=mnemonic))


def run_project(payload):
    settings = get_artifact_settings()
    params = [x.split('=') for x in payload]

    result = run_artifact(
        settings['rnkr']['mnemonic'],
        dict(zip([x[0] for x in params], [x[1] for x in params])),
        settings['config'].get('auth', 'token')
    )

    print json.dumps(result, sort_keys=True, indent=4)


def status_project():
    settings = get_artifact_settings()

    print json.dumps(
        get_artifact(
            settings['artifact']['pk'],
            settings['config'].get('auth', 'token')
        ),
        sort_keys=True,
        indent=4
    )


def upload_project():
    settings = get_artifact_settings()

    # build a payload from the rnkr file
    payload = copy.copy(settings['rnkr'])

    # create a zip with the code
    file_name = create_project_zip(payload['mnemonic'])
    with open(file_name, "rb") as fh:
        code = base64.b64encode(fh.read())

    payload['code'] = code

    __store_artifact(create_artifact(
        payload, settings['config'].get('auth', 'token')))
