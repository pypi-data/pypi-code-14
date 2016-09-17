# -*- coding: utf-8 -*-


class NoCustomSettingError(Exception):
    """It is not set value"""


class NoCustomSettingModuleError(Exception):
    """Cannot import custom settings module"""


class CustomSettingTypeError(TypeError, ValueError):
    """Cannot import custom settings module"""
