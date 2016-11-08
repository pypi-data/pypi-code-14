import logging

from django.contrib.auth.models import Group
from django.dispatch import receiver

from opencred.settings import SETTINGS

try:
    from account.signals import password_changed as accounts_password_changed
except ImportError:
    accounts_password_changed = None

try:
    from allauth.account.signals import password_changed as allauth_password_changed
    from allauth.account.signals import password_reset as allauth_password_reset
except ImportError:
    allauth_password_changed = None
    allauth_password_reset = None

logger = logging.getLogger(__name__)

GROUP = None


def load_group():
    global GROUP
    if not GROUP:
        GROUP, _ = Group.objects.get_or_create(name=SETTINGS.OPENCRED_RESTRICTED_GROUP)


def unrestrict_user(user):
    if not user:
        return

    logger.info('User %s changed its password and is no longer restricted', user)
    load_group()
    user.groups.remove(GROUP)


if accounts_password_changed:
    @receiver(accounts_password_changed, dispatch_uid="opencred-accounts-password-change-signal")
    def accounts_password_changed_listener(sender, user, **kwargs):
        unrestrict_user(user)

if allauth_password_changed:
    @receiver(allauth_password_changed, dispatch_uid="opencred-allauth-password-change-signal")
    def allauth_password_changed_listener(sender, user, **kwargs):
        unrestrict_user(user)

if allauth_password_reset:
    @receiver(allauth_password_reset, dispatch_uid="opencred-allauth-password-reset-signal")
    def allauth_password_reset_listener(sender, user, **kwargs):
        unrestrict_user(user)
