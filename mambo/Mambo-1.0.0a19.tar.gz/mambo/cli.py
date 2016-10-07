"""
________________________________________________________________________________

 /$$      /$$  /$$$$$$  /$$      /$$ /$$$$$$$   /$$$$$$
| $$$    /$$$ /$$__  $$| $$$    /$$$| $$__  $$ /$$__  $$
| $$$$  /$$$$| $$  \ $$| $$$$  /$$$$| $$  \ $$| $$  \ $$
| $$ $$/$$ $$| $$$$$$$$| $$ $$/$$ $$| $$$$$$$ | $$  | $$
| $$  $$$| $$| $$__  $$| $$  $$$| $$| $$__  $$| $$  | $$
| $$\  $ | $$| $$  | $$| $$\  $ | $$| $$  \ $$| $$  | $$
| $$ \/  | $$| $$  | $$| $$ \/  | $$| $$$$$$$/|  $$$$$$/
|__/     |__/|__/  |__/|__/     |__/|_______/  \______/


https://github.com/mardix/mambo

________________________________________________________________________________
"""

import os
import re
import sys
import traceback
import logging
import importlib
import pkg_resources
import click
import yaml
import functools
import sh
from werkzeug import import_string
from .__about__ import *

CWD = os.getcwd()
SKELETON_DIR = "skel"
APPLICATION_DIR = "%s/application" % CWD
APPLICATION_DATA_DIR = "%s/_data" % APPLICATION_DIR
APPLICATION_BABEL_DIR = "%s/babel" % APPLICATION_DATA_DIR

class MamboCLI(object):
    """
    For command line classes in which __init__ contains all the functions to use

    example

    class MyCLI(MamboCLI):
        def __init__(self):

            @cli.command()
            def hello():
                click.echo("Hello world")

            @cli.command()
            @click.argument("name")
            def say_my_name(name):
                click.echo("My name is %s" % name)
    """
    pass


def get_project_dir_path(project_name):
    return "%s/%s" % (APPLICATION_DIR, project_name)


def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    dest = (dest + "/" + os.path.basename(src)).rstrip("/")
    if pkg_resources.resource_isdir("mambo", src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + "/" + res, dest)
    else:
        if not os.path.isfile(dest) \
                and os.path.splitext(src)[1] not in [".pyc"]:
            with open(dest, "wb") as f:
                f.write(pkg_resources.resource_string(__name__, src))
        else:
            print("File exists: %s " % dest)


def create_project(project_name, no_assets=True, no_installed_apps=True):
    """
    Create the project
    """
    project_dir = get_project_dir_path(project_name)
    init_tpl = pkg_resources.resource_string(__name__, '%s/init.py' % (SKELETON_DIR))
    app_tpl = pkg_resources.resource_string(__name__, '%s/serve.py' % (SKELETON_DIR))
    propel_tpl = pkg_resources.resource_string(__name__, '%s/propel.yml' % (SKELETON_DIR))
    config_tpl = pkg_resources.resource_string(__name__, '%s/config.py' % (SKELETON_DIR))
    config_installed_apps_tpl = pkg_resources.resource_string(__name__, '%s/config_installed_apps.tpl' % (SKELETON_DIR))
    config_project_tpl = pkg_resources.resource_string(__name__, '%s/config_project.py' % (SKELETON_DIR))
    model_tpl = pkg_resources.resource_string(__name__, '%s/models.py' % (SKELETON_DIR))
    gitignore_tpl = pkg_resources.resource_string(__name__, '%s/gitignore' % (SKELETON_DIR))
    views_tpl = pkg_resources.resource_string(__name__, '%s/views.py' % (SKELETON_DIR))
    babel_tpl = pkg_resources.resource_string(__name__, '%s/babel.cfg' % (SKELETON_DIR))

    if not no_installed_apps:
        config_tpl = config_tpl.replace("##INSTALLED_APPS##", config_installed_apps_tpl)

    serve_file = "%s/serve.py" % CWD
    requirements_txt = "%s/requirements.txt" % CWD
    propel_yml = "%s/propel.yml" % CWD
    config_py = "%s/config.py" % APPLICATION_DIR
    model_py = "%s/models.py" % APPLICATION_DIR
    babel_cfg = "%s/babel.cfg" % APPLICATION_DIR
    gitignore = "%s/.gitignore" % CWD
    views = "%s/views.py" % project_dir
    config_project_py = "%s/config.py" % project_dir
    init_py = "%s/__init__.py" % APPLICATION_DIR

    dirs = [
        APPLICATION_DIR,
        APPLICATION_DATA_DIR,
        project_dir
    ]
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)

    files = [
        ("%s/__init__.py" % project_dir, "# Mambo"),
        (init_py, init_tpl),
        (config_py, config_tpl),
        (model_py, model_tpl),
        (serve_file, app_tpl.format(project_name=project_name)),
        (requirements_txt, "%s~=%s" % (__title__, __version__)),
        (propel_yml, propel_tpl.format(project_name=project_name)),
        (gitignore, gitignore_tpl),
        (views, views_tpl),
        (config_project_py, config_project_tpl),
        (babel_cfg, babel_tpl)
    ]
    for f in files:
        if not os.path.isfile(f[0]):
            with open(f[0], "wb") as f0:
                f0.write(f[1])

    if not no_assets:
        copy_resource("%s/assets/" % SKELETON_DIR, project_dir)

    copy_resource("%s/_data/" % SKELETON_DIR, APPLICATION_DATA_DIR)

# ------------------------------------------------------------------------------
serve = None


def get_propel_config(cwd, key):
    with open("%s/%s" % (cwd, "propel.yml")) as f:
        config = yaml.load(f)
    return config.get(key)


def get_push_remotes_list(cwd, key=None):
    """
    Returns the remote hosts in propel
    :param cwd:
    :param key:
    :param file:
    :return: list
    """
    config = get_propel_config(cwd, "deploy-remotes")
    return config[key] if key else [v for k, l in config.items() for v in l]


def git_push_to_master(cwd, hosts, name="all", force=False):
    """
    To push to master
    :param cwd:
    :param hosts:
    :param force:
    :return:
    """

    def process_output(line):
        print(line)

    with sh.pushd(cwd):
        name = "mambo_deploy_%s" % name

        if sh.git("status", "--porcelain").strip():
            raise Exception("Repository is UNCLEAN. Commit your changes")

        remote_list = sh.git("remote").strip().split()
        if name in remote_list:
            sh.git("remote", "remove", name)
        sh.git("remote", "add", name, hosts[0])

        if len(hosts) > 1:
            for h in hosts:
                sh.git("remote", "set-url", name, "--push", "--add", h)

        _o = ["push", name, "master"]
        if force:
            _o.append("--force")
        sh.git(*_o, _out=process_output)
        sh.git("remote", "remove", name)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def catch_exception(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            print("-" * 80)
            print("Exception Uncaught")
            print("-" * 80)
            print(ex)
            print("-" * 80)
    return decorated_view


def cwd_to_sys_path():
    sys.path.append(CWD)


def project_name(name):
    return re.compile('[^a-zA-Z0-9_]').sub("", name)


def header(title=None):
    print(__doc__)
    print("v. %s" % __version__)
    print("_" * 80)
    if title:
        print("** %s **" % title)


def build_assets(app):
    from webassets.script import CommandLineEnvironment
    assets_env = app.jinja_env.assets_environment
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.build()


@click.group()
def cli(): pass


@cli.command("create")
@click.argument("app_name")
@click.option("--no-assets", "-x", is_flag=True)
@click.option("--no-installed-apps", "-z", is_flag=True)
@catch_exception
def create(app_name, no_assets, no_installed_apps):
    """  Create a new Application in the current directory """

    app = project_name(app_name)

    header("Creating new app ...")
    print("")
    print("- Name: %s " % app)

    create_project(app, no_assets, no_installed_apps)

    print("")
    print("----- That was so Mambo! ----")
    print("")
    print("- Your new Mambo app [ %s ] has been created" % app)
    print("- Location: [ application/%s ]" % app)
    print("")
    print("> What's next?")
    print("- Edit the config [ application/config.py ] ")
    print("- If necessary edit and run the command [ mambo setup ]")
    print("- Launch app on development mode, run [ app='%s' mambo serve ]" % app)
    print("")
    print("*" * 80)


@cli.command("serve")
@click.option("--port", "-p", default=5000)
@catch_exception
def server(port):
    """ Serve application in development mode """

    header("Serving application in development mode ... ")
    print("")
    print("- Port: %s" % port)
    print("")
    cwd_to_sys_path()
    serve.app.run(debug=True, host='0.0.0.0', port=port)

@cli.command("syncdb")
def syncdb():
    """ Sync database Create new tables etc... """

    print("Syncing up database...")
    cwd_to_sys_path()
    serve = import_string("serve")
    if serve.app.db and serve.app.db.Model:
        serve.app.db.create_all()
        for m in serve.app.db.Model.__subclasses__():
            if hasattr(m, "_syncdb"):
                print("Sync up model: %s ..." % m.__name__)
                getattr(m, "_syncdb")()

    print("Done")


@cli.command("assets2s3")
@catch_exception
def assets2s3():
    """ Upload assets files to S3 """
    import flask_s3

    header("Assets2S3...")
    print("")
    print("Building assets files..." )
    print("")
    build_assets(serve.app)
    print("")
    print("Uploading assets files to S3 ...")
    flask_s3.create_all(serve.app)
    print("")


@cli.command("deploy")
@click.option("--remote", "-r", default=None)
@click.option("--force", "-f", is_flag=True, default=False)
@catch_exception
def deploy(remote, force):
    """ To deploy application to a git repository """

    remote_name = remote or "ALL"
    print("Deploying application to remote: %s " % remote_name)
    print("...")
    hosts = get_push_remotes_list(CWD, remote or None)
    git_push_to_master(cwd=CWD, hosts=hosts, name=remote_name, force=force)
    print("Done!")
    
@cli.command()
def version():
    print("-" * 80)
    print(__version__)
    print("-" * 80)

# @cli.command("babel-build")
# def babelbuild():
#     print("Babel Build....")
#     #sh.pybabel()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def cmd():
    """
    Help to run the command line
    :return:
    """
    global serve

    if os.path.isfile(os.path.join(os.path.join(CWD, "serve.py"))):
        cwd_to_sys_path()
        serve = import_string("serve")
    else:
        print("-" * 80)
        print("** Missing << 'serve.py' >> @ %s" % CWD)
        print("-" * 80)

    [cmd(cli.command, click) for cmd in MamboCLI.__subclasses__()]
    cli()

