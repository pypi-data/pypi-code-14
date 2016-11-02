import datetime
import flask_login
from flask_login import current_user
import flask_login
from flask import current_app
from mambo import (register_package, get_config, abort, send_mail, url_for, views, 
                   models, utils, request, redirect, flash, session, emit_signal)
from mambo.exceptions import AppError
from mambo.core import get_installed_app_options
import signals
import exceptions

register_package(__package__)

__version__ = "1.0.0"

ROLES_SUPERADMIN = ["SUPERADMIN"]
ROLES_ADMIN = ROLES_SUPERADMIN + ["ADMIN"]
ROLES_MANAGER = ROLES_ADMIN + ["MANAGER"]
ROLES_CONTRIBUTOR = ROLES_MANAGER + ["EDITOR", "CONTRIBUTOR"]
ROLES_MODERATOR = ROLES_CONTRIBUTOR + ["MODERATOR"]


def main(app, **kwargs):

    @app.before_request
    def force_password_change():
        _ = _get_app_options().get("require_password_change_exclude_endpoints")
        _ = [] if not isinstance(_, list) else _

        exclude_endpoints = ["static", "ContactPage:index", "Index:index",
                             "AuthLogin:logout"] + _

        if current_user and current_user.is_authenticated:
            if request.endpoint \
                    and request.endpoint not in exclude_endpoints:
                if request.endpoint != "AuthAccount:change_password" \
                        and session_get_require_password_change():
                    flash("Password Change is required", "info")
                    return redirect(views.AuthAccount.change_password)

_app_options = None


def _get_app_options():
    global _app_options
    if not _app_options:
        _app_options = get_installed_app_options(__name__)
    return _app_options


def is_authenticated():
    """ A shortcut to check if a user is authenticated """
    return current_user.is_authenticated


def not_authenticated():
    """ A shortcut to check if user not authenticated."""
    return not is_authenticated()


def get_user(id):
    """
    To get a user by id
    :param id:
    :return: AuthUser object
    """
    return models.AuthUser.get(id)


def get_random_password(length=8):
    return utils.generate_random_string(length)


# ------------------------------------------------------------------------------
#
def visible_to(*roles):
    """
    This is a @nav_menu specific function to set the visibility of menu based on
    roles
    :param roles:
    :return: callback fn
    """
    if is_authenticated():
        return True if current_user.has_any_roles(*roles) else False
    return False


# Alias to visible_to
visible_to_superadmins = lambda: visible_to(*ROLES_SUPERADMIN)
visible_to_admins = lambda: visible_to(*ROLES_ADMIN)
visible_to_managers = lambda: visible_to(*ROLES_MANAGER)
visible_to_contributors = lambda: visible_to(*ROLES_CONTRIBUTOR)
visible_to_moderators = lambda: visible_to(*ROLES_MODERATOR)
visible_to_authenticated = lambda: is_authenticated()
visible_to_notauthenticated = lambda: not_authenticated()

# ------------------------------------------------------------------------------
# SIGNUP + LOGIN
def session_login(user_login):
    """
    Login the user to the session
    :param user_login: AuthUserLogin
    :return:
    """
    user_login.user.update(last_login=datetime.datetime.now())
    flask_login.login_user(user_login.user)


def login_with_email(email, password, verify_email=False):
    """
    To login a user with email
    :param email:
    :param password:
    :return:
    """
    def cb():
        userl = models.AuthUserLogin.get_by_email(email)
        if userl and userl.password_hash \
                and userl.password_matched(password):
            if verify_email and not userl.email_verified:
                raise exceptions.VerifyEmailError()
            session_login(userl)
            return userl
        return None
    return signals.on_login(cb)


def signup_with_email(email, password, name, role=None):
    """
    To create a new email login
    :param email:
    :param password:
    :param name:
    :return: AuthUserLogin
    """
    def cb():
        return models\
            .AuthUserLogin.new(login_type=models.AuthUserLogin.TYPE_EMAIL,
                               email=email,
                               password=password.strip(),
                               user_info={
                                    "name": name,
                                    "contact_email": email,
                                    "role": role
                               })
    return signals.on_signup(cb)

# ------------------------------------------------------------------------------
# EMAIL SENDING

def send_mail_password_reset(user_login):
    """
    To reset a user password and send email
    :param user_login: UserLogin object
    :return:
    """
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    delivery = options.get("reset_password_method") or "token"
    token_ttl = get_config("reset_password_token_ttl") or 60
    email_template = options.get("reset_password_email_template") or "reset-password.txt"
    new_password = None

    if delivery.lower() == "token":
        token = user_login.set_temp_login(token_ttl)
        url = url_for(views.AuthLogin.reset_password, token=token, _external=True)
    else:
        new_password = user_login.change_password(random=True)
        url = url_for(views.AuthLogin.index, _external=True)

    send_mail(template=email_template,
              method_=delivery.lower(),
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              url=url,
              new_password=new_password)


def _create_user_login_verify_email(user_login):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    token_ttl = options.get("verify_email_token_ttl") or (60 * 24)
    token = user_login.set_email_verified_token(token_ttl)
    url = url_for(views.AuthLogin.verify_email, token=token, _external=True)
    return token, url


def send_mail_verification_email(user_login):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError("Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    email_template = options.get("verify_email_template") or "verify-email.txt"
    token, url = _create_user_login_verify_email(user_login)

    send_mail(template=email_template,
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              verify_url=url)


def send_mail_signup_welcome(user_login):
    if user_login.login_type != models.AuthUserLogin.TYPE_EMAIL:
        raise AppError(
            "Invalid login type. Must be the type of email to be sent email to")

    options = _get_app_options()
    verify_email = options.get("verify_email") or False
    email_template = options.get("verify_signup_email_template") or "verify-signup-email.txt"
    token, url = _create_user_login_verify_email(user_login)

    send_mail(template=email_template,
              to=user_login.email,
              name=user_login.user.name,
              email=user_login.email,
              verify_url=url,
              verify_email=verify_email)


def session_set_require_password_change(change=True):
    session["auth:require_password_change"] = change

def session_get_require_password_change():
    return session.get("auth:require_password_change")


# ------------------------------------------------------------------------------
# CLI
from mambo.cli import MamboCLI

class CLI(MamboCLI):
    def __init__(self, command, click):
        @command("auth:create-super-admin")
        @click.argument("email")
        def create_super_admin(email):
            """
            To create a super admin by providing the email address
            """
            print("-" * 80)
            print("Mambo Auth: Create Super Admin")
            print("Email: %s" % email)
            try:
                password = get_random_password()
                nl = create_new_login(email=email,
                                      password=password,
                                      name="SuperAdmin",
                                      role=models.AuthRole.SUPERADMIN)
                nl.update(require_password_change=True)
                print("Password: %s" % password)
            except Exception as e:
                print("ERROR: %s" % e)

            print("Done!")

        @command("auth:reset-password")
        @click.argument("email")
        def reset_password(email):
            """
            To reset password by email
            """
            print("-" * 80)
            print("Mambo Auth: Reset Password")
            try:
                ul = models.AuthUserLogin.get_by_email(email)

                if not ul:
                    raise Exception("Email '%s' doesn't exist" % email)
                print(ul.email)
                password = get_random_password()
                ul.change_password(password)
                ul.update(require_password_change=True)
                print("Email: %s" % email)
                print("New Password: %s" % password)
            except Exception as e:
                print("ERROR: %s" % e)

            print("Done!")

        @command("auth:user-info")
        @click.option("--email")
        @click.option("--id")
        def reset_password(email=None, id=None):
            """
            Get the user info by email or ID
            """
            print("-" * 80)
            print("Mambo Auth: User Info")
            print("")
            try:
                if email:
                    ul = models.AuthUserLogin.get_by_email(email)
                    if not ul:
                        raise Exception("Invalid Email address")
                    user_info = ul.user
                elif id:
                    user_info = models.AuthUser.get(id)
                    if not user_info:
                        raise Exception("Invalid User ID")

                k = [
                    ("ID", "id"), ("Name", "name"), ("First Name", "first_name"),
                    ("Last Name", "last_name"), ("Signup", "created_at"),
                    ("Last Login", "last_login"), ("Signup Method", "signup_method"),
                    ("Is Active", "is_active")
                ]
                print("Email: %s" % user_info.get_email_login().email)
                for _ in k:
                    print("%s : %s" % (_[0], getattr(user_info, _[1])))

            except Exception as e:
                print("ERROR: %s" % e)

            print("")
            print("Done!")


# ---

from .decorators import *
