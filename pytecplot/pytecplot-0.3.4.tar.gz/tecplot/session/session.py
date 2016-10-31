from ..tecutil import _tecinterprocess
import atexit


@atexit.register  # Automatically call stop() when Python is unloaded
def stop():
    """Releases the |Tecplot License| and shuts down |Tecplot Engine|.

    This shuts down the |Tecplot Engine| and releases the |Tecplot License|.
    Call this function when your script is finished using |PyTecplot|.
    Calling this function is not required. If you do not call this function,
    it will be called automatically when your script exists. However, the
    |Tecplot License| will not be released until you call this function.

    Note that stop() may only be called once during the life of a Python
    session. If it has already been called, subsequent calls do nothing.

    See also: `tecplot.session.acquire_license()`,
    `tecplot.session.release_license()`.

    Example:

        .. code-block:: python
            :emphasize-lines: 4

            >>> import tecplot
            >>> # Do useful things with pytecplot
            >>> tecplot.session.stop() # Shutdown the tecplot and release license
    """
    _tecinterprocess.stop()


def acquire_license():
    """Attempts to acquire the |Tecplot License|

    Call this function to attempt to acquire a |Tecplot License|. If
    |Tecplot Engine| is not started, this function will start the
    |Tecplot Engine| before attempting to acquire a license.

    This function can be used to re-acquire a license that was released with
    `tecplot.session.release_license`.

    If the |Tecplot Engine| is currently running, and a
    |Tecplot License| has already been acquired, this function has no effect.

    Licenses may be acquired and released any number of times during the same
    Python session.

    Raises `TecplotLicenseError` if a valid license could not be acquired.

    See also: `tecplot.session.release_license()`

    Example:

        .. code-block:: python

        >>> import tecplot
        >>> # Do useful things
        >>> tecplot.session.release_license()
        >>> # Do time-consuming things not related to |PyTecplot|
        >>> tecplot.session.acquire_license()  # re-acquire the license
        >>> # Do useful |PyTecplot| related things.
    """
    _tecinterprocess.acquire_license()


def release_license():
    """Attempts to release the |Tecplot License|

    Call this to release a |Tecplot License|. Normally you do not need to call
    this function since `tecplot.session.stop()` will call it for you when your script
    exists and the Python interpreter is unloaded.

    This function can be used to release a license so that the license is
    available to other instances of |Tecplot 360 EX|.

    If the |Tecplot License| has already been released, this function has
    no effect.

    Licenses may be acquired and released any number of times during the same
    Python session.

    See also: `tecplot.session.acquire_license()`

    Example:

        .. code-block:: python

        >>> import tecplot
        >>> # Do useful things
        >>> tecplot.session.release_license()
        >>> # Do time-consuming things not related to |PyTecplot|
        >>> tecplot.session.acquire_license()  # re-acquire the license
        >>> # Do useful |PyTecplot| related things.
    """
    _tecinterprocess.release_license()
