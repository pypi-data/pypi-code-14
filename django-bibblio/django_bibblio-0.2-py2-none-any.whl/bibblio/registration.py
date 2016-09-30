from .datastructures import ContentItem

__all__ = ["registry", "autodiscover", "BibblioAdapter", ]


class Registry(object):
    """
    A Registry object encapsulates a mapping of Django Models to the Taxonomy
    Adapter for them.
    """
    def __init__(self):
        self._registry = {}

    def register(self, model, func):
        """
        Register a function to adapt the Model.
        """
        self._registry[model] = func

    def adapter_for_instance(self, model):
        return self._registry[model.__class__](model)


registry = Registry()


def autodiscover():
    from django.utils.module_loading import autodiscover_modules

    autodiscover_modules('adapters', register_to=registry)


class BibblioAdapter(object):
    missing_attribute_value = ''
    raise_error_on_missing = False

    def __init__(self, instance):
        self.instance = instance

    def as_content_item(self):
        """
        Convert to a ContentItem
        """
        return ContentItem(instance=self.instance)

    @property
    def _content_type(self):
        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get_for_model(self.instance)

    @property
    def _pk(self):
        return self.instance.pk

    def __getattr__(self, name):
        """
        Try to get ``name`` from a get_FOO method or the original object

        Remember: __getattr__ is only called when ``name`` is not found.

        This method could get recursively called twice, the first time, it will
        add ``get_`` to the beginning at try again. Then it tries the self.instance
        """
        if name.startswith("get_"):
            try:
                import re
                original_name = re.sub(r"^get_", "", name)
                return getattr(self.instance, original_name)
            except AttributeError:
                if self.raise_error_on_missing:
                    raise
                else:
                    return self.missing_attribute_value
        else:
            accessor_name = "get_%s" % name
            get_value = getattr(self, accessor_name, False)
            if callable(get_value):
                return get_value()
            else:
                return get_value
