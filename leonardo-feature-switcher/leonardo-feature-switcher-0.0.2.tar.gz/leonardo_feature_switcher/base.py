
import importlib

from django.utils import six
from django.core.exceptions import ImproperlyConfigured

CACHED_FUNCTIONS = {}

FEATURE_SWITCHERS = None


def get_feature_switchers():
    """lazy feature switchers
    """

    global FEATURE_SWITCHERS

    if not FEATURE_SWITCHERS:

        from leonardo import leonardo

        FEATURE_SWITCHERS = leonardo.config.get_attr('feature_switchers')

        if not FEATURE_SWITCHERS:
            raise Exception("Add feature_switchers to LEONARDO_CONF_SPEC")

        if not isinstance(FEATURE_SWITCHERS, dict):
            raise ImproperlyConfigured(
                "FEATURE_SWITCHERS must be a dictionary")

    return FEATURE_SWITCHERS


def is_on(request, flag, *args, **kwargs):

    try:
        flag_func = get_feature_switchers()[flag]
    except KeyError:
        raise Exception("Missing %s in LEONARDO_FEATURE_SWITCHERS" % flag)
    else:
        if isinstance(flag_func, six.string_types):

            if flag_func not in CACHED_FUNCTIONS:

                string_module = '.'.join(flag_func.split(".")[0:-1])
                string_func = flag_func.split(".")[-1]

                flag_module = importlib.import_module(string_module)
                real_func = getattr(flag_module, string_func)

                CACHED_FUNCTIONS[flag_func] = real_func
                flag_func = real_func

            else:
                flag_func = CACHED_FUNCTIONS[flag_func]

    return flag_func(request, *args, **kwargs)


def is_off(request, flag, **kwargs):
    return not is_on(request, flag, **kwargs)
