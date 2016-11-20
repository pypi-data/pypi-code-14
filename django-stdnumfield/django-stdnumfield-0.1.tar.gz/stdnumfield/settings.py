from django.conf import settings

from stdnumfield import STDNUM_FORMATS


_STDNUMFIELD = {
    'DEFAULT_FORMATS': STDNUM_FORMATS.keys(),
}

try:
    _STDNUMFIELD.update(settings.STDNUMFIELD)
except AttributeError:
    pass

# locals().update(_STDNUMFIELD)  # let's keep things autocomplete-friendly:

DEFAULT_FORMATS = _STDNUMFIELD['DEFAULT_FORMATS']
