# -*- coding: utf-8 -*-

import re


class SinicValidate(object):
    def __init__(self):
        # Refer: http://www.oschina.net/code/snippet_238351_48624
        # Refer: http://baike.baidu.com/view/12118274.htm
        # Refer: http://news.imobile.com.cn/articles/2016/0204/164468.shtml
        self.ChinaMobile = r'^134\d{8}$|^(?:13[5-9]|147|15[0-27-9]|178|18[2-478])\d{8}$'
        self.ChinaUnion = r'^(?:13[0-2]|145|1[578][56])\d{8}$'
        self.ChinaTelcom = r'^(?:133|153|17[37]|18[019])\d{8}$'
        self.OtherTelphone = r'^17[01]\d{8}$'  # 虚拟运营商

        self.email_regex = r'^.+@([^.@][^@]+)$'

    def phone(self, message, china_mobile=None, china_union=None, china_telcom=None, other_telphone=None):
        """
        Validates a phone number.
        :param message:
        :param china_mobile:
        :param china_union:
        :param china_telcom:
        :param other_telphone:
        :return:
        """
        isChinaMobile = isChinaUnion = isChinaTelcom = isOtherTelphone = False
        if re.match(china_mobile or self.ChinaMobile, message):
            isChinaMobile = True
        elif re.match(china_union or self.ChinaUnion, message):
            isChinaUnion = True
        elif re.match(china_telcom or self.ChinaTelcom, message):
            isChinaTelcom = True
        elif re.match(other_telphone or self.OtherTelphone, message):
            isOtherTelphone = True
        return {
            'isPhone': isChinaMobile or isChinaUnion or isChinaTelcom or isOtherTelphone,
            'isChinaMobile': isChinaMobile,
            'isChinaUnion': isChinaUnion,
            'isChinaTelcom': isChinaTelcom,
            'isOtherTelphone': isOtherTelphone,
        }

    def email(self, message, regex=None):
        """
        Validates an email address.
        :param message:
        :param regex:
        :return:
        """
        return re.match(regex or self.email_regex, message)


class SinicSimpleValidate(object):
    def __init__(self):
        self.phone_regex = r'^1\d{10}$'

    def phone(self, message, regex=None):
        """
        Simple validates a phone number.
        :param message:
        :param regex:
        :return:
        """
        return re.match(regex or self.phone_regex, message)


validate = SinicValidate()
phone = validate.phone
email = validate.email

simple = SinicSimpleValidate()
