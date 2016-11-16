from django.conf import settings

from . import constants


STATUS_CHECKS = getattr(
    settings,
    'DJANGO_SITE_HEALTH_STATUS_CHECKS',
    (constants.DATABASE, constants.FILESYSTEM)
)

FAILURE_CHECKS = getattr(
    settings,
    'DJANGO_SITE_HEALTH_FAILURE_CHECKS',
    (constants.DATABASE,)
 )
