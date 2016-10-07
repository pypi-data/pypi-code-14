"""
Tecplot Exceptions
==================

The class hierarchy for |PyTecplot| exceptions are as follows. Exceptions in
parentheses are Python built-ins from which the |PyTecplot| exceptions
derive. One can use either the Python native errors or the more specific
"Tecplot" errors to catch exceptions::

    TecplotError (Exception)
     +--- TecplotInitializationError (ImportError)
     |     +--- TecplotLicenseError
     |     +--- TecplotLibraryNotLoadedError
     |     +--- TecplotLibraryNotFoundError
     +--- TecplotLogicError (AssertionError)
     +--- TecplotLookupError (LookupError)
     |     +--- TecplotIndexError (IndexError)
     |     +--- TecplotKeyError (KeyError)
     +--- TecplotOSError (OSError)
     +--- TecplotRuntimeError (RuntimeError)
     |     +--- TecplotNotImplementedError (NotImplementedError)
     +--- TecplotSystemError (SystemError)
     |     +--- TecplotMacroError
     +--- TecplotTypeError (TypeError)
     +--- TecplotValueError (ValueError)
"""

from builtins import super


class TecplotError(Exception):
    """Tecplot error."""


class TecplotAttributeError(AttributeError):
    """Undefined attribute."""


class TecplotInitializationError(TecplotError, ImportError):
    """Tecplot engine could not be initialized."""


class TecplotLibraryNotFoundError(TecplotInitializationError):
    """Interprocess library was not found in PATH or DY/LD_LIBRARY_PATH."""


class TecplotLibraryNotLoadedError(TecplotInitializationError):
    """Interprocess library could not be loaded."""


class TecplotLicenseError(TecplotInitializationError):
    """Invalid or missing Tecplot license."""


class TecplotLogicError(TecplotError, AssertionError):
    """TecUtil method contract was violated."""


class TecplotLookupError(TecplotError, LookupError):
    """Could not find requested object."""


class TecplotIndexError(TecplotLookupError, IndexError):
    """Index out of range or invalid."""


class TecplotKeyError(TecplotLookupError, KeyError):
    """Key not found."""


class TecplotOSError(TecplotError, OSError):
    """Operating system error."""


class TecplotOverflowError(TecplotError, OverflowError):
    """Integer value out of required range."""


class TecplotRuntimeError(TecplotError, RuntimeError):
    """PyTecplot post-initialization error."""


class TecplotNotImplementedError(TecplotRuntimeError, NotImplementedError):
    """Requested operation is planned but not implemented."""


class TecplotSystemError(TecplotError, SystemError):
    """Tecplot Engine error or failure."""
    def __init__(self, message=None):
        from tecplot.tecutil import _tecinterprocess
        msgs = []
        if _tecinterprocess.last_message:
            msgs.append(_tecinterprocess.last_message.message)
        if message:
            msgs.append(str(message))
        super().__init__('\n'.join(msgs))


class TecplotMacroError(TecplotSystemError):
    """Macro command failed to execute."""


class TecplotTypeError(TecplotError, TypeError):
    """Incorrect or invalid type was used."""


class TecplotValueError(TecplotError, ValueError):
    """Bad value."""
