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

    try:
        token = ctx.obj.token(auth=(email, password))
    except click.ClickException as e:
        if e.response.status_code == 401:
            raise click.ClickException('Invalid Credentials')

        raise

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
@click.option('--scope', '-s', multiple=True)
@click.pass_context
def token(ctx, scope):
    """Generate an authentication token"""
    click.echo(ctx.obj.token(scopes=scope))


@cli.command('app')
@click.argument('app')
@click.option('--create', is_flag=True)
@click.option('--delete', is_flag=True)
@click.pass_context
def app(ctx, app, create, delete):
    """View or manage a specific application"""

    if create:
        payload = ctx.obj.create_app(app)
        click.echo('{name} ({web_url}) has been created.'.format(**payload))
        return

    if delete:
        click.confirm('Are you sure you want to delete {}?'.format(app), abort=True)
        ctx.obj.delete_app(app)
        click.echo('{} has been deleted.'.format(app))
        return

    payload = ctx.obj.app(app)

    click.echo('{} - {}'.format(payload['name'], payload['web_url']))

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
            web_url = alias.get('web_url', None)
            domains = alias.get('domains', None)

            click.echo('- Name: {}'.format(name))

            if web_url:
                click.echo('  URL: {}'.format(web_url))

            if version:
                click.echo('  Version: {}'.format(version))

            if domains:
                click.echo('  Domains:')

                for domain in domains:
                    click.echo('    - {}'.format(domain['domain']))


@cli.command('apps')
@click.pass_context
def apps(ctx):
    """List your Rigid apps"""

    apps = ctx.obj.apps()

    for app in apps:
        click.echo(app['name'])

    if len(apps) == 0:
        click.echo("You don't have any apps yet.")


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
        new_app = ctx.obj.create_app(app)
        app = new_app['name']
        click.echo('Application {} has been created.'.format(app))
    else:
        deploy.validate(app)

    if verbose:
        files = deploy.collect_files()
        click.echo('{} source files:'.format(len(files)))

        for name in files:
            click.echo('- {}'.format(name))

    uploader, length = deploy.upload(app)

    with click.progressbar(length=length, label='Uploading Source') as progress:
        source_uuid = uploader(progress.update)

    version_uuid = deploy.upload_version(app, source_uuid)

    click.echo('Version {} has been created'.format(version_uuid))

    with click.progressbar(length=100, label='Promoting to {}'.format(alias)) as progress:
        counter = 0

        while True:
            try:
                ctx.obj.promote(app, alias, version_uuid, config)
                break
            except click.ClickException as e:
                progress.update(1)

                if hasattr(e, 'response') and e.response.status_code == 400:
                    payload = e.response.json()

                    if len(payload) == 1 and 'version' in payload:
                        pass
                    else:
                        raise
                else:
                    raise

            counter += 1
            time.sleep(2)

            if counter % 2:
                time.sleep(2)

    click.echo('{} ({}) has been deployed.'.format(app, alias))


@cli.command('domains')
@click.option('--app', '-a', required=True)
@click.option('--alias', default='production')
@click.argument('domain')
@click.option('--add', is_flag=True)
@click.option('--remove', is_flag=True)
@click.pass_context
def domains(ctx, app, alias, domain, add, remove):
    """
    Manage custom domains for an app
    """

    if not add and not remove:
        raise click.ClickException('--add or --remove must be provided')

    if add:
        ctx.obj.add_domain(app, alias, domain)
        click.echo('{} has been added to {}.'.format(domain, app))

    if remove:
        ctx.obj.remove_domain(app, alias, domain)
        click.echo('{} has been removed from {}.'.format(domain, app))


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
