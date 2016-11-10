import inspect
import logging

from django.forms import BaseForm
from django.forms.widgets import Widget
from django.utils.module_loading import import_module
from django.conf import settings

from form_renderers import as_div


logger = logging.getLogger("logger")


# Add a required="required" attribute to widgets if applicable. This is a safe
# blanket policy.
def decorate(meth):
    def decorator(context, *args, **kwargs):
        di = meth(context, *args, **kwargs)
        if context.is_required and ("required" not in di):
            di["required"] = "required"
        return di
    return decorator


logger.info("Patching Widget.build_attrs")
Widget.build_attrs = decorate(Widget.build_attrs)


# Add the default as_div renderer
logger.info("Adding BaseForm.as_div")
BaseForm.as_div = as_div


# Add renderers from installed apps. Reverse the order so topmost apps can
# override other similarly named renderers.
for app_name in reversed(settings.INSTALLED_APPS):
    try:
        module = import_module(app_name + ".form_renderers")
    except ImportError:
        continue
    for name, func in inspect.getmembers(module, inspect.isfunction):
        logger.info("Adding BaseForm.%s" % name)
        setattr(BaseForm, name, func)
