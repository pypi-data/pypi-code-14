import functools
import flask_login
from flask_login import current_user
from flask import current_app
from mambo import (register_package, get_config, abort, send_mail, url_for, views, 
                   models, utils, request, redirect, flash, session)
from mambo.exceptions import AppError

register_package(__package__)

__version__ = "1.0.0"

ROLES_ADMIN = ["SUPERADMIN", "ADMIN"]
ROLES_MANAGER = ROLES_ADMIN + ["MANAGER"]
ROLES_CONTRIBUTOR = ROLES_MANAGER + ["EDITOR", "CONTRIBUTOR"]
ROLES_CONTRIBUTOR = ROLES_CONTRIBUTOR + ["MODERATOR"]


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
        c = get_config("INSTALLED_APPS")
        if c:
            for k in c:
                if isinstance(k, dict) and "name" in k and k["name"] == __name__:
                    _app_options = k["options"] if "options" in k else {}
                    break
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


def authenticate_login(email, password):
    pass


def get_random_password(length=8):
    return utils.generate_random_string(length)


def create_new_login(email, password, name, role=None):
    """
    To create a new email login
    :param email:
    :param password:
    :param name:
    :return: AuthUserLogin
    """
    return models\
        .AuthUserLogin.new(login_type=models.AuthUserLogin.TYPE_EMAIL,
                           email=email,
                           password=password.strip(),
                           user_info={
                                "name": name,
                                "contact_email": email,
                                "role": role
                           })


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
    return session["auth:require_password_change"]

# ---------------------- DECORATORS --------------------- #

def authenticated(func):
    """
    A wrapper around the flask_login.login_required.
    But it also checks the presence of the decorator: @unauthenticated
    On a "@authenticated" class, method containing "@unauthenticated" will
    still be able to access without authentication
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if "unauthenticated" not in utils.get_decorators_list(func) \
                and not_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def unauthenticated(func):
    """
    Dummy decorator. @authenticated will inspect the method
    to look for this decorator
    Use this decorator when you want do not require login in a "@authenticated" class/method
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view


def logout_user(f):
    """
    Decorator to logout user
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        flask_login.logout_user()
        return f(*a, **kw)
    return deco


def require_verified_email(f):
    pass


def require_login_allowed(f):
    """
    Decorator to abort if login is not allowed
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        if not _get_app_options().get("allow_login"):
            abort(403, "Login not allowed. Contact admin if it's a mistake")
        return f(*a, **kw)
    return deco


def require_signup_allowed(f):
    """
    Decorator to abort if signup is not allowed
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        if not _get_app_options().get("allow_signup"):
            abort(403, "Signup not allowed. Contact admin if it's a mistake")
        return f(*a, **kw)
    return deco


def require_social_login_allowed(f):
    """
    Decorator to abort if social login is not allowed
    :param f:
    :return:
    """
    @functools.wraps(f)
    def deco(*a, **kw):
        if not _get_app_options().get("allow_social_login"):
            abort(403, "Social login not allowed. Contact admin if it's a mistake")
        return f(*a, **kw)
    return deco


def accepts_roles(*roles):
    """
    A decorator to check if user has any of the roles specified

    @roles_accepted('superadmin', 'admin')
    def fn():
        pass
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if is_authenticated():
                if not current_user.has_any_roles(*roles):
                    return abort(403)
            else:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def accepts_admin_roles(func):
    """
    Decorator that accepts only admin roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_ADMIN)(func)(*args, **kwargs)
    return decorator


def accepts_manager_roles(func):
    """
    Decorator that accepts only manager roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_MANAGER)(func)(*args, **kwargs)
    return decorator


def accepts_contributor_roles(func):
    """
    Decorator that accepts only contributor roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_CONTRIBUTOR)(func)(*args, **kwargs)
    return decorator


def accepts_moderator_roles(func):
    """
    Decorator that accepts only moderator roles
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return accepts_roles(*ROLES_MODERATOR)(func)(*args, **kwargs)
    return decorator

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
