import ConfigParser
import os
import json
import subprocess
import glob

from jinja2 import Environment, PackageLoader

from .consts import RNKR_FILE, RNKRRC_FILE, RNKR_ARTIFACT_FILE


def create_project_zip(mnemonic):
    file_name = '{0}.zip'.format(mnemonic)
    subprocess.call(['zip', '-r', file_name] + glob.glob('*'))
    return file_name


def render_template(template, context, out):
    env = Environment(loader=PackageLoader('rnkrcli', 'templates'))
    template = env.get_template(template)

    with open(out, 'wb') as fh:
        fh.write(template.render(context))


def get_artifact_settings():
    result = {}

    if not os.path.isfile(RNKR_FILE):
        raise Exception('could not find `rnkr` file in current directory')

    with open(RNKR_FILE, 'r') as f:
        result['rnkr'] = json.load(f)

    if os.path.isfile(RNKR_ARTIFACT_FILE):
        with open(RNKR_ARTIFACT_FILE) as f:
            result['artifact'] = json.load(f)

    config_path = os.path.join(os.path.expanduser('~'), RNKRRC_FILE)
    if not os.path.isfile(config_path):
        raise Exception('could not find rnkrrc file in home directory')

    # parse the rc file for credentials
    config = ConfigParser.SafeConfigParser()
    config.read(config_path)

    result['config'] = config
    return result
