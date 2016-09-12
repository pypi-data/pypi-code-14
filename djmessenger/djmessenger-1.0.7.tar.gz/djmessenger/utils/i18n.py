# -*- coding: utf-8 -*-
from ..models import FBUserProfile
import gettext
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


def install_user_locale(psid):
    """
    Install the locale for the user psid, if not able to load it, reset

    @param psid:
    @return:
    """
    try:
        user = FBUserProfile.objects.get(pk=psid)
        lang = user.locale
        logger.debug('locale dirs: %s' % settings.LOCALE_PATHS)
        for locale_dir in settings.LOCALE_PATHS:
            zh = gettext.translation('django',
                                     localedir=locale_dir,
                                     languages=[lang])
            zh.install()
            logger.debug('Successfully installed language %s for user %s'
                         % (lang, psid))
    except Exception as e:
        logger.debug('Installing locale for user %s failed because %s, '
                     'resetting...' % (psid, e))
        reset_locale()


def reset_locale():
    logger.debug('Resetting locale...')
    _ = lambda s: s
