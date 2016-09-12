# -*- coding: utf-8 -*-
class DJMException(Exception):
    """
    Base Exception for DJM
    """
    pass


class DJMInvalidConfigException(DJMException):
    """
    This exception will be raised if user tried to do something that breaks the
    assumption made by Facebbok. For example, threading setting greeting text
    can have only one, if the user tried to add more, raise this exception
    """
    pass


class DJMInvalidValueException(DJMException):
    pass
