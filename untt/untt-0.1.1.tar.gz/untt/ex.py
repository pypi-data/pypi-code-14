"""
This module is where the untt error definitions live.
"""


class UnttError(Exception):
    """
    Root error class for untt.
    """
    pass


class DefinitionError(UnttError):
    """
    Raises when there is an entity definition error.
    """
    pass


class ValidationError(UnttError):
    """
    Raises when there is a validation error.
    """
    pass
