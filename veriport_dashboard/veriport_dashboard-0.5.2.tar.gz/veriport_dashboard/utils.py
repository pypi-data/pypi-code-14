from django.apps import apps
from django.conf import settings


def generate_queryset_ids(objects):
    """
    Returns IDs of queryset objects given
    """
    for item in objects:
        yield item.id


def get_report_model():
    """
    Returns the Veriport Report model
    """
    report_app_model = getattr(settings, "VERIPORT_REPORT_MODEL",
        "veriport_dashboard.Report")
    report_app, report_model = report_app_model.split(".")
    return apps.get_model(report_app, report_model)


def get_account_model():
    """
    Returns the Veriport Account model
    """
    account_app_model = getattr(settings, "VERIPORT_ACCOUNT_MODEL",
        "veriport_dashboard.Account")
    account_app, account_model = account_app_model.split(".")
    return apps.get_model(account_app, account_model)


def get_user_model():
    """
    Returns the registered User model
    """
    user_app_model = getattr(settings, "AUTH_USER_MODEL",
        "auth.User")
    user_app, user_model = user_app_model.split(".")
    return apps.get_model(user_app, user_model)
