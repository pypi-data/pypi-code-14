# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.conf import settings
from .rest_client import RestClient

VERIFIEDUSER_TYPE = (
    (0, u"实名认证"),
    (1, u"上传认证"),
)

VERIFIEDUSER_STATUS = (
    (0, u"认证成功"),
    (1, u"待审核"),
    (2, u"废弃"),
    (4, u"认证失败")
)

BANKVERIFY_TYPE = (
    (0, u"存折"),
    (1, u"借记卡"),
    (2, u"信用卡")
)

BANKVERIFY_STATUS = (
    (0, u"成功"),
    (2, u"未使用"),
    (4, u"失败"),
)

JavaCommonRestClient = RestClient(
    settings.JAVA_COMMON_SYSTEM['host'],
    settings.JAVA_COMMON_SYSTEM['base_url'],
    settings.JAVA_COMMON_SYSTEM['protocol'],
    oauth_app_id=settings.JAVA_COMMON_SYSTEM['appid'],
    oauth_app_secret=settings.JAVA_COMMON_SYSTEM['secret'],
    logger=logging.getLogger("djdg_common_verify"),
)