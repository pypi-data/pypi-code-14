import os
import time
import netrc

import click
import requests
import yaml

from rigid import __version__
from rigid.api import Client
from rigid.deploy import Deploy


def load_config(config_file, alias):
    config = None

    if not config_file:
        if os.path.exists('.rigid-{}.yaml'.format(alias)):
            config_file = '.rigid-{}.yaml'.format(alias)
        elif os.path.exists('.rigid.yaml'):
            config_file = '.rigid.yaml'

    if config_file:
        with open(config_file) as fp:
            config = yaml.safe_load(fp)

    return config


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
    ctx.obj = Client()


@cli.command('login')
@click.pass_context
def login(ctx):
    """Login with your Rigid credentials"""

    click.echo('Enter your Rigid credentials.')

    email = click.prompt('Email', type=str)
    password = click.prompt('Password', type=str, hide_input=True)

    token = ctx.obj.token(auth=(email, password))

    path = os.path.expanduser('~/.rigid')

    try:
        os.mkdir(path)
    except:
        pass

    with open(os.path.join(path, 'credentials'), 'w') as fp:
        fp.write(token)


@cli.command('logout')
def logout():
    path = os.path.expanduser('~/.rigid')
    os.remove(os.path.join(path, 'credentials'))


@cli.command('whoami')
@click.pass_context
def whoami(ctx):
    """Show your Rigid login"""
    click.echo(ctx.obj.user()['email'])


@cli.command('token')
@click.pass_context
def token(ctx):
    """Generate an authentication token"""
    click.echo(ctx.obj.token())


@cli.command('apps')
@click.argument('app', required=False)
@click.pass_context
def apps(ctx, app):
    """List your Rigid apps"""

    if not app:
        apps = ctx.obj.apps()

        for app in apps:
            click.echo(app['name'])

        return

    payload = ctx.obj.app(app)

    click.echo(app)

    if 'versions' in payload:
        click.echo()
        click.echo('Versions')

        for version in payload['versions']:
            click.echo('- ' + version['uuid'])

    if 'aliases' in payload:
        click.echo()
        click.echo('Aliases')

        for alias in payload['aliases']:
            name = alias['name']
            version = alias.get('version', None)

            if version:
                click.echo('- {} (version: {})'.format(name, version))
            else:
                click.echo('- {}' + name)


@cli.command('deploy')
@click.argument('source', type=click.Path(exists=True))
@click.option('--app', '-a', required=False)
@click.option('--alias', default='production')
@click.option('--create', default=False, is_flag=True)
@click.option('--config', type=click.Path(exists=True))
@click.option('--verbose', default=False, is_flag=True)
@click.pass_context
def deploy(ctx, source, app, alias, create, config, verbose):
    """Deploy a new version"""

    if app is None and not create:
        raise click.MissingParameter(param_type='option "--app" / "-a"')

    config = load_config(config, alias)
    deploy = Deploy(ctx.obj, source)

    if create:
        with click.progressbar(length=1, label='Creating Application') as progress:
            new_app = ctx.obj.create_app(app)
            app = new_app['name']
            progress.update(1)

        click.echo('Application {} has been created.'.format(app))
    else:
        deploy.validate(app)

    if verbose:
        files = deploy.collect_files()
        click.echo('{} source files:'.format(len(files)))

        for name in files:
            click.echo('- {}'.format(name))

    with click.progressbar(length=100, label='Uploading Source') as progress:
        source_uuid = deploy.upload(app)
        progress.update(5)
        version_uuid = deploy.upload_version(app, source_uuid)
        progress.update(100)

    click.echo('Version {} has been created'.format(version_uuid))

    with click.progressbar(length=100, label='Promoting to {}'.format(alias)) as progress:
        counter = 0

        while True:
            try:
                ctx.obj.promote(app, alias, version_uuid, config)
                progress.update(100)
                break
            except click.ClickException as e:
                if hasattr(e, 'response') and e.response.status_code == 400:
                    payload = e.response.json()

                    if len(payload) == 1 and 'version' in payload:
                        pass
                    else:
                        raise
                else:
                    raise

            counter += 1
            progress.update(counter)
            time.sleep(2)

            if counter % 2:
                time.sleep(2)

    click.echo('Deployed to {} to {}'.format(app, alias))


@cli.command('promote')
@click.option('--app', '-a', required=True)
@click.option('--alias', default='production')
@click.option('--config', type=click.Path(exists=True))
@click.argument('version')
@click.pass_context
def promote(ctx, app, alias, config, version):
    """Promote a version to an alias."""

    config = load_config(config, alias)
    payload = ctx.obj.promote(app, alias, version, config)
    click.echo('{}/{} is now running {}.'.format(app, alias, payload['version']))
