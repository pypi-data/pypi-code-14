import inspect
import logging

from django.forms import BaseForm
from django.forms.widgets import Widget
try:
    from django.forms.boundfield import BoundField
except ImportError:
    # Django 1.6
    from django.forms.forms import BoundField
from django.utils.module_loading import import_module
from django.conf import settings

from form_renderers import SETTINGS, as_div


logger = logging.getLogger("logger")


# Add a required="required" attribute and a classname describing the input to
# widgets if applicable. This is a safe blanket policy.
def decorate_a(meth):
    def decorator(context, *args, **kwargs):
        di = meth(context, *args, **kwargs)
        if context.is_required and ("required" not in di):
            di["required"] = "required"
        if "class" not in di:
            di["class"] = ""
        di["class"] = di["class"] + " " +context.__class__.__name__ + "-input"
        return di
    return decorator


logger.info("Patching Widget.build_attrs")
Widget.build_attrs = decorate_a(Widget.build_attrs)


# BEM - Add a CSS class describing the field.
def decorate_b(meth):
    def decorator(context, *args, **kwargs):
        result = meth(context, *args, **kwargs)
        result += "Form-item Field %s-item" % context.field.__class__.__name__
        if context.field.widget.is_required:
            result += " Field--required"
        return result
    return decorator


if SETTINGS["enable-bem-classes"]:
    logger.info("Patching BoundField.css_classes")
    BoundField.css_classes = decorate_b(BoundField.css_classes)


# BEM - Add a CSS class for the label. This is a safe blanket policy.
def decorate_c(meth):
    def decorator(context, contents=None, attrs=None, label_suffix=None):
        if attrs is None:
            attrs = {"class": ""}
        if "class" in attrs:
            attrs["class"] += " "
        attrs["class"] += "Field-label"
        return meth(context, contents, attrs, label_suffix)
    return decorator

if SETTINGS["enable-bem-classes"]:
    logger.info("Patching BoundField.label_tag")
    BoundField.label_tag = decorate_c(BoundField.label_tag)


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
