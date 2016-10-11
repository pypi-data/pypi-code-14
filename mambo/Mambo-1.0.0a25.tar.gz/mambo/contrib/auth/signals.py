from mambo import emit_signal, models
from blinker import Namespace

ns = Namespace()


@emit_signal(namespace=ns)
def on_signup(cb):
    """
    Emit a signal when signing up
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


@emit_signal(namespace=ns)
def on_login(cb):
    """
    Emit signal when logged in
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


@emit_signal(namespace=ns)
def on_logout(cb):
    """
    :param cb: callback function to execute
    :return: Current user
    """
    return cb()


@emit_signal(namespace=ns)
def on_account_info_change(cb):
    """
    :param cb: callback function to execute
    :return:
    """
    return cb()

@emit_signal(namespace=ns)
def on_login_change(cb):
    """
    :param cb: callback function to execute
    :return:
    """
    return cb()


@emit_signal(namespace=ns)
def on_password_change(cb):
    """
    :param cb: callback function to execute
    :return:
    """
    return cb()

@emit_signal(namespace=ns)
def on_verify_email(cb):
    """
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()

@emit_signal(namespace=ns)
def on_profile_image_change(cb):
    """
    :param cb: callback function to execute
    :return:
    """
    return cb()

@emit_signal(namespace=ns)
def on_reset_password(cb):
    """
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


@emit_signal(namespace=ns)
def on_confirm_email(cb):
    """
    :param cb: callback function to execute
    :return: AuthUserLogin
    """
    return cb()


