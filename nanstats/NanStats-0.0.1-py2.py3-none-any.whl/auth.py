from nanigans.config import AUTH

class Credentials(object):
    """ The <[Credentials Object]> is an adapted version of
    https://github.com/faif/python-patterns/blob/master/borg.py.

    It shares credentials amongst its instances to allow users to set default 
    credentials in a Python environment or set up credentials in a config.py file.

    """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self._credentials = AUTH if all(AUTH.values()) else None

    @property
    def credentials(self):
        return self._credentials

    def __repr__(self):
        if self._credentials:
            return "<Credentials Object [Signed]>"
        else:
            return "<Credentials Object [Unsigned]>"

    def __str__(self):
        return "<[Credentials Object]>"
