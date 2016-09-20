#! /user/bin/env python
# -*- coding:utf-8 -*-

class ADCloudError(Exception):
    pass


class ADCFileUnFoundError(ADCloudError):
    pass

class ADCMissingRequiredOptionError(ADCloudError):
    pass

class ADCTypeError(ADCloudError):
    pass

class ADCInvalidSettingError(ADCloudError):
    pass

class ADCSettingValueTypeError(ADCloudError):
    pass