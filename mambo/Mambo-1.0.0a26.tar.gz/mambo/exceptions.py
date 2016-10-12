"""
Mambo

Error

"""


class MamboError(Exception):
    """
    This exception is not reserved, but it used for all Mambo exception.
    It helps catch Core problems.
    """
    pass


class AppError(MamboError):
    """
    Use this exception in your application level.
    """
    pass


class ModelError(AppError):
    """
    Use this exception in your model level.
    """
    pass





