import functools
import flask_login
import signals
import inspect
from . import (_get_app_options, is_authenticated, not_authenticated,
               ROLES_ADMIN, ROLES_MANAGER, ROLES_CONTRIBUTOR, ROLES_MODERATOR)
from mambo import utils, abort

__all__ = [
    "authenticated",
    "unauthenticated",
    "logout_user",
    "require_verified_email",
    "require_login_allowed",
    "require_signup_allowed",
    "require_social_login_allowed",
    "accepts_roles",
    "accepts_admin_roles",
    "accepts_manager_roles",
    "accepts_contributor_roles",
    "accepts_moderator_roles"
]

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
            return flask_login.current_app.login_manager.unauthorized()
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
        signals.on_logout(lambda: flask_login.current_user)
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
                if not flask_login.current_user.has_any_roles(*roles):
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

