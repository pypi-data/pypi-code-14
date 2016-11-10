import logging

from django.forms import Form
from django.forms.widgets import Widget

from form_renderers.renderers import as_div


logger = logging.getLogger("logger")


def decorate(meth):
    def decorator(context, *args, **kwargs):
        di = meth(context, *args, **kwargs)
        if context.is_required and ("required" not in di):
            di["required"] = "required"
        return di
    return decorator


logger.info("Patching Widget.build_attrs")
Widget.build_attrs = decorate(Widget.build_attrs)


logger.info("Adding Form.as_div")
Form.as_div = as_div
