"""
Applause CLI Tool.
~~~~~~~~~~~~~~~~~~~
"""
import logging
import click
import os

from applause.ais import InvalidAppKeyError, InvalidCustomerKeyError
from . import settings
from .session import AuthSession
from .errors import InvalidLogin
from .utils import enable_debug_mode, requires_login
from .beta import ApplauseBETA
from .sdk import ApplauseSDK
from .ais import ApplauseAIS
from .param import PathString, StringParamType

# `prog` & `version` will be auto detected by clicked based on setup.py
VERSION_MESSAGE = '%(prog)s version %(version)s Applause Inc. 2016. All rights reserved'
USERNAME_ENV_VAR_NAME = 'APPLAUSE_USERNAME'
PASSWORD_ENV_VAR_NAME = 'APPLAUSE_PASSWORD'


@click.group(context_settings={"help_option_names": ['-h', '--help']})
@click.version_option(message=VERSION_MESSAGE)
@click.option('--debug', is_flag=True, help="Enable extended logging")
def main(debug):
    """
    Applause CLI tool, Applause Inc. All rights reserved.
    """
    if debug:
        enable_debug_mode()


@main.command()
@click.option('--username', '-u', help="Login")
@click.option('--password', '-p', help="Password")
@click.option('--store-password', '-s', help="Store password", is_flag=True, default=False)
def login(username=None, password=None, store_password=False):
    """
    Authenticate to the Applause CLI tool and persist your credentials file
    for later usage. Using the store password flag means that your credentials will be stored in plain text
    and can be later used for refreshing the access token should it choose to expire.
    Otherwise only the currently stored access token will be used for accessing Applause services
    and when it expires (after 2 weeks), you will be asked to login again.
    """
    # Get user credentials
    username = username or os.environ.get(USERNAME_ENV_VAR_NAME, None) or click.prompt("Username")
    password = password or os.environ.get(PASSWORD_ENV_VAR_NAME, None) or click.prompt("Password", hide_input=True)
    store_password = bool(store_password)

    # Make sure they are valid & store data for later usage
    auth = AuthSession(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, load_cookie=False)

    try:
        click.echo("Logging in...")
        auth.login(username=username, password=password, remember_password=store_password)
        click.echo("Success. Cookie stored at: {path}".format(path=auth.config_path))
    except InvalidLogin as e:
        logging.debug("Login error: {error}".format(error=e))
        click.echo("Invalid credentials")


@main.command()
def logout():
    """
    Revoke user access tokens & purge any session specific configuration files.
    """
    auth = AuthSession(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, load_cookie=False)
    click.echo("Logging out...")
    auth.logout()
    click.echo("Cookie removed.")


@main.command()
def account():
    """
    Print information about currently logged in user.
    """
    auth = AuthSession(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET)
    if auth.is_active():
        click.echo("Currently logged in user: {username}".format(username=auth.username))
    else:
        click.echo("No user session. Please login.")


@main.group()
def sdk():
    """
    Applause SDK product specific operations.
    """


@sdk.command(name='distribute')
@click.argument('company_id')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option('--changelog', '-c', type=PathString(exists=True), help="Release notes file for the uploaded build")
@click.option(
    '--emails', '-e', type=PathString(exists=True), multiple=True,
    help="List of emails to distribute the build to. "
         "If path, each email should be on a new line.",
)
@requires_login
def distribute(session, company_id, app_id, path, changelog, emails):
    sdk = ApplauseSDK(session.get_session())
    sdk.distribute(company_id, app_id, path, changelog, emails)
    click.echo("Distributed.")


@sdk.command(name='upload')
@click.argument('company_id')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option('--set-as-current', is_flag=True, default=False, help="Set item build as current build for application")
@click.option('--changelog', '-c', type=PathString(exists=True), help="Release notes file for the uploaded build")
@requires_login
def upload_to_sdk(session, company_id, app_id, path, changelog, set_as_current):
    # company_id is just for preserving cli usage
    sdk = ApplauseSDK(session.get_session())
    sdk.upload(app_id, path, changelog, set_as_current)
    click.echo("Uploaded.")


@main.group()
def beta():
    """
    Applause MBM product specific operations.
    """


@beta.command(name='upload')
@click.argument('company_id')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option('--set-as-current', is_flag=True, default=False, help="Set item build as current build for application")
@click.option('--changelog', '-c', type=PathString(exists=True), help="Release notes file for the uploaded build")
@requires_login
def upload_to_beta(session, company_id, app_id, path, changelog, set_as_current):
    # company_id is just for preserving cli usage
    mbm = ApplauseBETA(session.get_session())
    mbm.upload(app_id, path, changelog, set_as_current)
    click.echo("Uploaded.")


@beta.command(name='distribute')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option(
    '--emails', '-e', type=PathString(exists=True), multiple=True,
    help="List of emails to distribute the build to. "
         "If path, each email should be on a new line.",
)
@click.option(
    '--groups', '-g', type=PathString(exists=True), multiple=True,
    help="List of groups names to distribute the build to"
)
@click.option(
    '--changelog', '-c', type=PathString(exists=True),
    help="Release notes file for the uploaded build"
)
@click.option(
    '--sent-from', '-s', type=PathString(exists=True),
    help="E-mail address used as the sender"
)
@click.option('--set-as-current', is_flag=True, default=False, help="Set item build as current build for application")
@requires_login
def distribute_to_beta(session, app_id, path, groups, emails, changelog, sent_from, set_as_current):
    # company_id is just for preserving cli usage
    mbm = ApplauseBETA(session.get_session())
    mbm.validate(groups, emails)
    mbm.distribute(app_id, path, groups, emails=emails, changelog=changelog, sent_from=sent_from, set_as_current=set_as_current)
    click.echo("Uploaded.")


@main.group()
def ais():
    """
    Applause AIS (SDK injection) product specific operations.
    """


@ais.command(name='instrument')
@click.argument('path', type=click.Path(exists=True))
@click.option('--customer-key', '-c', type=StringParamType(),
              help="Service access token. Please contact support to get one.")
@click.option('--app-key', '-k', type=StringParamType(), help="Application app key passed to the mobile SDK.")
@click.option('--output', '-o', type=StringParamType(), help="Path to the output file.")
@requires_login
def instrument(session, path, customer_key, app_key, output):
    ais = ApplauseAIS(session.get_session(), customer_key=customer_key)

    try:
        output_path = ais.instrument(path, app_key, output)
    except InvalidAppKeyError as e:
        click.echo("Error: Please make sure you provided a valid app key: {}.\n Details: {}".format(app_key, e))
    except InvalidCustomerKeyError:
        click.echo("Error: Please make sure you provided a valid customer key!")
    else:
        click.echo("Done. Output file created: {}".format(output_path))
        click.echo(click.style("Please remember to sign your build before distributing it!", fg='yellow', bold=True))


if __name__ == '__main__':
    main()
